from datetime import datetime
import os.path
import json
from salal.core.log import log
from salal.core.config import config

class DependencyManager:

    separator = ':'
    
    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        log.message('DEBUG', 'Initializing dependency tracking')
        # ONLY PARTIALLY IMPLEMENTED, DOESN'T LOAD A BUILD LOG

        # initialize utility variables
        cls.cur_target = None
        cls.cur_source = None
            
        # initialize the update queue
        cls.update_queue = {'timestamp': datetime.now(), 'files': dict(), 'variables': dict()}

    #---------------------------------------------------------------------------
    
    @classmethod
    def needs_build (cls, target_file, source_file):
        # JUST A STUB FOR NOW, NEED TO IMPLEMENT THE CHECKS
        return True

    #---------------------------------------------------------------------------

    @classmethod
    def start_build_tracking (cls, target_file, source_file):
        cls.cur_target = target_file
        cls.cur_source = source_file
        cls.update_queue['files'][target_file + cls.separator + source_file] = {
            "variables": dict(),
            "templates": []
        }
    
    #---------------------------------------------------------------------------

    @classmethod
    def template_used (cls, template_file):
        cls.update_queue['files'][cls.cur_target + cls.separator + cls.cur_source]['templates'].append(template_file)

    #---------------------------------------------------------------------------

    @classmethod
    def variable_used (cls, variable_name):
        cls.update_queue['files'][cls.cur_target + cls.separator + cls.cur_source]['variables'][variable_name] = None
        cls.update_queue['variables'][variable_name] = None

    #---------------------------------------------------------------------------
    
    @classmethod
    def stop_build_tracking (cls):
        cls.cur_target = None
        cls.cur_source = None
        
    #---------------------------------------------------------------------------
    
    @classmethod
    def write_log (cls):
        log.message('DEBUG', 'Updating build log')
        # JUST A STUB FOR NOW, DOESN'T ACTUALLY WRITE A FILE
        
    #---------------------------------------------------------------------------
    
dependencies = DependencyManager
