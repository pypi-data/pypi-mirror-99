import os

from cbase import config
from cbase import utils

class Repo:
    ###########################################################################
    def __init__(self, cb):
        """
        ConnectMe Repo class
        """

        self.cb = cb

        self.path = ""
        self.path_to_desc = ""

        self.meta = {}

    ###########################################################################
    def init(self, path="", name="", uid="", desc=""):
        """
        Find CM-compatible repository in a given or current path

        Args:
             path (str): path to a repo (optional).
                         If path is not specified, attempt to find repo 
                         in the current directory and above.

        """

        # Init meta
        meta = {}

        # Check which path to use
        if path == "":
            path = os.getcwd()

        # Search if there is a repo in this path
        path_to_desc = os.path.join(path, self.cb.cfg['repo_desc_file'], path)
        if os.path.isfile(path_to_desc):
            r = io.load_json_or_yaml(path_to_desc)
            if r['return']>0: return r

            meta = r['data']

        else:
            # Create paths if needed
            r = utils.check_and_create_dir(path)
            if r['return']>0: return r

            # Init new one
            if uid=='':
                r = utils.gen_uid()
                uid = r['uid']

            if name == '':
                name = uid
            
            meta={'name':name,
                  'uid':uid,
                  'desc':desc}
                       
            path_to_desc = os.path.join(path, self.cb.cfg['repo_desc_file'])

            r = utils.save_json_or_yaml(path_to_desc, meta, sort_keys=True)
            if r['return']>0: return r

            # Add path to repos in CM class
            r = self.register_path(path)
            if r['return'] >0 : return r

        # Finish init
        self.path = path
        self.path_to_desc = path_to_desc
        self.meta = meta

        return {'return':0}

    ###########################################################################
    def where(self, path=""):    
        """
        Find CM-compatible repository in a given or current path

        Args:
             path (str): path to a repo (optional).
                         If path is not specified, attempt to find repo 
                         in the current directory and above.

        """

        # Find repository in a path
        r = io.find_file_in_dir_and_above(config.REPO_DESC_FILE, path)

        if r['return'] == 0:
            r['path_to_desc'] = os.path.join(r['path'], config.REPO_DESC_FILE)

        return r

    ###########################################################################
    def load(self, path=""):    
        """
        Load CM-compatible repository from a given or current path

        Args:
             path (str): path to a repo (optional).
                         If path is not specified, attempt to find repo 
                         in the current directory and above.

        """

        # Find repository in a path
        r = self.where(path)
        if r['return'] > 0 : return r

        path = r['path']
        self.path = path
        
        path_to_desc = r['path_to_desc']
        self.path_to_desc = path_to_desc

        r = io.load_json_or_yaml(path_to_desc)
        if r['return'] > 0: return r

        self.desc = r['data']

        return r

    ###########################################################################
    def register_path(self, path):
        """
        Register path with repository.
        
        Args:
             path (str): path to a CM repository

        """

        found = False
        for x in self.cb.repos:
            try:
                if os.path.samefile(x['path'], path):
                    found = True
                    break
            except:
                pass

        if not found:
            self.cb.repos.append({'path':path})

        # Save file
        r = utils.save_json_or_yaml(self.cb.rt['file_repo_list'], self.cb.repos, sort_keys=True)
        if r['return']>0: return r

        return {'return':0}
