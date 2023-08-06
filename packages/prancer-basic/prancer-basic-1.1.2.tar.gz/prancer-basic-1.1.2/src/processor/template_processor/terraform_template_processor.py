from processor.logging.log_handler import getlogger
from processor.template_processor.base.base_template_processor import TemplateProcessor
from processor.templates.terraform.terraform_parser import TerraformTemplateParser
from processor.helper.json.json_utils import json_from_file
from processor.helper.hcl.hcl_utils import hcl_to_json

logger = getlogger()

class TerraformTemplateProcessor(TemplateProcessor):
    """
    
    Base Template Processor for process template 
    """

    def __init__(self, node, **kwargs):
        super().__init__(node, tosave=False, **kwargs)
        self.exclude_directories = ["modules"]
    
    def is_template_file(self, file_path):
        """
        check for valid template file for parse terraform template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "tf":
            json_data = hcl_to_json(file_path)
            return True if (json_data and ("resource" in json_data or "module" in json_data)) else False
        elif len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "json":
            json_data = json_from_file(file_path, escape_chars=['$'])
            return True if (json_data and ("resource" in json_data or "module" in json_data)) else False
        return False
    
    def is_parameter_file(self, file_path):
        """
        check for valid variable file for parse terraform template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] in ["tf", "tfvars"]:
            json_data = hcl_to_json(file_path)
            return True if (json_data and not "resource" in json_data) else False
        elif len(file_path.split(".")) > 1 and [ele for ele in [".tfvars.json", ".tf.json"] if(ele in file_path)]:
            json_data = json_from_file(file_path, escape_chars=['$'])
            return True if (json_data and not "resource" in json_data) else False
        return False
    
    def generate_template_and_parameter_file_list(self, file_path, template_file, parameter_file_list, generated_template_file_list):
        """
        process template and parameter files and returns the generated template file list
        """
        paths = parameter_file_list + [template_file]
        template_json = self.process_template(paths)

        parameter_files = []
        for parameter_file in parameter_file_list:
            parameter_files.append(
                ("%s/%s" % (file_path, parameter_file)).replace("//", "/")
            )

        paths = parameter_files + [("%s/%s" % (file_path, template_file)).replace("//", "/")]
        if template_json:
            generated_template_file_list.append({
                "paths" : paths,
                "status" : "active",
                "validate" : self.node['validate'] if 'validate' in self.node else True
            })
        else:
            generated_template_file_list.append({
                "paths" : paths,
                "status" : "inactive",
                "validate" : self.node['validate'] if 'validate' in self.node else True
            })

    def process_template(self, paths):
        """
        process the files stored at specified paths and returns the template
        """
        template_json = None
        if paths and isinstance(paths, list):
            template_file_path = ""
            parameter_file_list = []
            
            for path in paths:
                file_path = '%s/%s' % (self.dir_path, path)
                logger.info("Fetching data : %s ", path)
                if self.is_template_file(file_path):
                    template_file_path = file_path
                if self.is_parameter_file(file_path):
                    parameter_file_list.append(file_path)

            if template_file_path:
                terraform_template_parser = TerraformTemplateParser(template_file_path,parameter_file=parameter_file_list)
                template_json = terraform_template_parser.parse()

                self.template_files = terraform_template_parser.template_file_list
                self.parameter_files = terraform_template_parser.parameter_file_list

        return template_json