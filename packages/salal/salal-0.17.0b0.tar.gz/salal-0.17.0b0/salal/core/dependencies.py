from datetime import datetime
import os.path
import json
from salal.core.log import log
from salal.core.config import config
from salal.core.utilities import utilities

class DependencyManager:

    separator = ':'
    
    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        log.message('DEBUG', 'Initializing dependency tracking')

        # read the build log
        cls.build_log_file = os.path.join(config.system['paths']['config_root'], config.system['paths']['build_log_dir'], config.system['profile'] + '.json')
        if os.path.isfile(cls.build_log_file):
            with open(cls.build_log_file, 'r') as build_log_fh:
                build_log = json.load(build_log_fh)
            cls.last_build_time = datetime.strptime(build_log['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            cls.file_log = build_log['files']
            cls.variable_log = build_log['variables']
            cls.template_log = set(build_log['templates'])
        else:
            cls.last_build_time = datetime.min
            cls.file_log = dict()
            cls.variable_log = dict()
            cls.template_log = set()

        # initialize utility variables
        cls.n_files_checked = 0
        cls.n_files_built = 0
        cls.cur_target = None
        cls.cur_source = None
        cls.cur_file_key = None
            
        # initialize the update queue
        cls.cur_build_time = datetime.now()
        cls.file_updates = dict()
        cls.variable_updates = dict()
        cls.template_updates = set()

        cls.file_check_flags = {file_ref:False for file_ref in cls.file_log.keys()}
        cls.variable_change_flags = cls.check_for_variable_changes(cls.variable_log, cls.variable_updates)
        cls.template_change_flags = cls.check_for_template_changes(cls.template_log)
    
    #---------------------------------------------------------------------------
    # For each variable in the log, we create a flag to indicate
    # whether the variabe has changed since the last build, which is
    # used to help determine when a source file should be rebuilt.
    @classmethod
    def check_for_variable_changes (cls, variable_log, variable_updates):
        variable_change_flags = dict()
        for variable in variable_log:
            # It's not necessarily an error if a variable from the
            # last build doesn't exist any more, because references to
            # that variable may also have been removed. So we don't
            # throw an error here, but we do warn and trigger a
            # rebuild of any source files that referenced the
            # variable.
            if not variable in config.project:
                log.message('WARN', 'Variable ' + variable + ' is in the build log but no longer exists')
                variable_change_flags[variable] = True
            elif variable_log[variable] != config.project[variable]:
                log.message('TRACE', 'Detected change to variable ' + variable)
                variable_change_flags[variable] = True
                variable_updates[variable] = config.project[variable]
            else:
                variable_change_flags[variable] = False
        return variable_change_flags
                    
    #---------------------------------------------------------------------------

    # For each template in the log, we create a flag to indicate
    # whether the template has changed since the last build, which is
    # used to help determine when a source file should be rebuilt.
    @classmethod
    def check_for_template_changes (cls, template_log):
        template_change_flags = dict()
        for template_file in template_log:
            # It's not necessarily an error if a template from the
            # last build doesn't exist any more, because references to
            # that template may also have been removed. So we don't
            # throw an error here, but we do warn trigger a rebuild of
            # any source files that referenced the template.
            if not os.path.isfile(template_file):
                log.message('WARN', 'Template ' + template_file + ' is in the build log but no longer exists')
                template_change_flags[template_file] = True
            else:
                template_mod_time = datetime.fromtimestamp(os.path.getmtime(template_file))
                if template_mod_time > cls.last_build_time:
                    log.message('TRACE', 'Detected change to template ' + template_file)
                    template_change_flags[template_file] = True
                else:
                    template_change_flags[template_file] = False
        return template_change_flags
                    
    #---------------------------------------------------------------------------
    
    @classmethod
    def needs_build (cls, target_file, source_file):
        cls.n_files_checked += 1
        target_key = target_file + cls.separator + source_file
        
        # Is this file in the build log? If not, rebuild, if yes, then
        # record that a build check was conducted for it and proceed.
        if target_key not in cls.file_log:
            log.message('TRACE', 'Target ' + target_file + ' is not in the build log, build required')
            return True
        else:
            cls.file_check_flags[target_key] = True

        # Does the target exist? If not, rebuild.
        if not os.path.isfile(target_file):
            log.message('TRACE', 'Target ' + target_file + ' does not exist, build required')
            return True

        # Is the source newer than the target? If so, rebuild.
        source_mod_time = datetime.fromtimestamp(os.path.getmtime(source_file))
        if source_mod_time > cls.last_build_time:
            log.message('TRACE', 'Source file ' + source_file + ' is newer than target ' + target_file + ', build required')
            return True

        # Have any referenced variables been changed? If so, rebuild.
        for variable in cls.file_log[target_key]['variables']:
            if cls.variable_change_flags[variable]:
                log.message('TRACE', 'Variable ' + variable + ' used by target ' + target_file + ' has changed, build required')
                return True

        # Have any referenced templates been changed? If so, rebuild.
        for template in cls.file_log[target_key]['templates']:
            if cls.template_change_flags[template]:
                log.message('TRACE', 'Template ' + template + ' used by target ' + target_file + ' has changed, build required')
                return True

        return False

    #---------------------------------------------------------------------------

    @classmethod
    def start_build_tracking (cls, target_file, source_file):
        cls.n_files_built += 1
        cls.cur_target = target_file
        cls.cur_source = source_file
        cls.cur_file_key = target_file + cls.separator + source_file
        if cls.cur_file_key not in cls.file_log:
            log.message('TRACE', 'Detected new build target ' + target_file + ', now tracking it')
        cls.file_updates[cls.cur_file_key] = {
            "target": target_file,
            "source": source_file,
            "variables": [],
            "templates": []
        }
    
    #---------------------------------------------------------------------------

    @classmethod
    def variable_used (cls, variable_name):
        if variable_name not in cls.file_updates[cls.cur_file_key]['variables']:
            cls.file_updates[cls.cur_file_key]['variables'].append(variable_name)
            if variable_name not in cls.variable_log and variable_name not in cls.variable_updates:
                log.message('TRACE', 'Detected use of new variable ' + variable_name + ', now tracking it');
                cls.variable_updates[variable_name] = config.project[variable_name] 

    #---------------------------------------------------------------------------

    @classmethod
    def variable_not_found (cls, variable_name):
        log.message('WARN', 'Encountered reference to undefined variable ' + variable_name)
    
    #---------------------------------------------------------------------------
    
    @classmethod
    def template_used (cls, template_file):
        if template_file not in cls.file_updates[cls.cur_file_key]['templates']:
            cls.file_updates[cls.cur_file_key]['templates'].append(template_file)
            if template_file not in cls.template_log and template_file not in cls.template_updates:
                log.message('TRACE', 'Detected use of new template ' + template_file + ', now tracking it');
                cls.template_updates.add(template_file) 
                
    #---------------------------------------------------------------------------

    @classmethod
    def stop_build_tracking (cls):
        cls.cur_target = None
        cls.cur_source = None
        cls.cur_file_key = None
        
    #---------------------------------------------------------------------------

    @classmethod
    def num_files_checked (cls):
        return cls.n_files_checked
    
    #---------------------------------------------------------------------------
    
    @classmethod
    def num_files_built (cls):
        return cls.n_files_built
    
    #---------------------------------------------------------------------------
    
    @classmethod
    def write_log (cls):
        log.message('DEBUG', 'Updating build log')
        
        # incorporate updates to the file, variable, and template logs
        cls.file_log.update(cls.file_updates)
        cls.variable_log.update(cls.variable_updates)
        cls.template_log.update(cls.template_updates)

        # remove entries for stale files (were in build log but no
        # longer part of the build)
        for file_ref in cls.file_check_flags:
            if not cls.file_check_flags[file_ref]:
                log.message('TRACE', 'Target ' + cls.file_log[file_ref]['target'] + ' is no longer part of the build, discontinuing tracking and deleting from build directory');
                if os.path.exists(cls.file_log[file_ref]['target']):
                    os.remove(cls.file_log[file_ref]['target'])
                cls.file_log.pop(file_ref)

        # remove build directories that are now empty
        empty_dirs = utilities.find_empty_subdirectories(config.system['paths']['profile_build_dir'])
        for dir in empty_dirs:
            log.message('TRACE', 'Build directory ' + dir + ' no longer contains anything, deleting')
            os.rmdir(dir)
                
        # remove variables from the log that aren't referenced by a
        # file anymore
        variables_referenced = set()
        for file_entry in cls.file_log.values():
            if 'variables' in file_entry:
                for variable in file_entry['variables']:
                    variables_referenced.add(variable)
        for variable in cls.variable_change_flags:
            if variable not in variables_referenced:
                log.message('TRACE', 'Variable ' + variable + ' is no longer part of the build, discontinuing tracking'); 
                cls.variable_log.pop(variable)

        # remove templates from the log that aren't referenced by a
        # file anymore
        templates_referenced = set()
        for file_entry in cls.file_log.values():
            if 'templates' in file_entry:
                for template in file_entry['templates']:
                    templates_referenced.add(template)
        for template in cls.template_change_flags:
            if template not in templates_referenced:
                log.message('TRACE', 'Template ' + template + ' is no longer part of the build, discontinuing tracking');
                cls.template_log.remove(template)

        # create the build log directory if it doesn't exist
        os.makedirs(os.path.join(config.system['paths']['config_root'], config.system['paths']['build_log_dir']), exist_ok = True)
        # write the file
        with open(cls.build_log_file, 'w') as build_log_fh:
            json.dump({'timestamp': cls.cur_build_time, 'files': cls.file_log, 'variables': cls.variable_log, 'templates': list(cls.template_log)}, build_log_fh, default=str)
        
    #---------------------------------------------------------------------------
    
dependencies = DependencyManager
