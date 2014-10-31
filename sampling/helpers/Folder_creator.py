'''
Created on Aug 4, 2013

@author: Emrah Cem{emrah.cem@utdallas.edu}
'''
import os
import logging

log = logging.getLogger(__name__)

__all__=['create_folder','create_sample_folder','create_sampler_folder','create_graph_folder','create_job_folder', 'create_population_folder','create_samplers_folder']

def create_job_folder(job_name, input_file):
    folder_postfix=1
    try:
        if os.path.exists(job_name):
            while os.path.exists(job_name+"_"+str(folder_postfix)):
                folder_postfix=folder_postfix+1
            os.makedirs(job_name+"_"+str(folder_postfix))
            created_folder_name=job_name+"_"+str(folder_postfix)
        else:
            os.makedirs(job_name)
            created_folder_name=job_name
        temp=os.getcwd()
        
        abs_path=os.path.abspath(input_file)
        new_path=os.path.split(abs_path)[0]+'/'+created_folder_name+'/'+input_file
        os.chdir(os.path.join(temp,created_folder_name))
        import shutil
        
        shutil.copyfile(abs_path , new_path)
    except Exception as e:
        log.exception(e)
    else:
        return True
#        print 'Job folder could not be created'
        #log.debug("Job folder could not be  created.")
        #log.debug(er)
#    else:
#        return True
    #finally:
    #    os.chdir(temp)

def create_folder(folder_name):#,log_message=None):
    try:
        temp=os.getcwd()
        log.debug('creating directory:'+os.path.join(os.getcwd(),folder_name))
        os.makedirs(os.path.join(temp,folder_name))
        os.chdir(os.path.join(temp,folder_name))
    except Exception as e:
        log.exception(e)
    else:
        return True


def create_samplers_folder():
    try:
        temp=os.getcwd()
        log.debug('creating directory:'+os.getcwd())
        os.makedirs(os.path.join(temp,'samplers'))
        os.chdir(os.path.join(temp,'samplers'))
    except Exception as e:
        log.exception(e)
    else:
        return True
    
def create_population_folder():
    try:
        temp=os.getcwd()
        log.debug('creating directory:'+os.getcwd())
        os.makedirs(os.path.join(temp,'population'))
        os.chdir(os.path.join(temp,'population'))
    except Exception as e:
        log.exception(e)
    else:
        return True


def create_graph_folder(G):
    try:
        temp=os.getcwd()
        os.makedirs(os.path.join(temp,G.graph['name']))
        os.chdir(os.path.join(temp,G.graph['name']))
        log.debug('creating directory:'+os.getcwd())
    except Exception as e:
        log.exception(e)
    else:
        return True

def create_sampler_folder(G,sampler):
   
    try:
        temp=os.getcwd()
        os.makedirs(os.path.join(temp,sampler.name))
        os.chdir(os.path.join(temp,sampler.name))
        log.debug('creating directory:'+os.getcwd())

    except Exception as e:
        log.exception(e)
    finally:
        return True


def create_sample_folder(sample_name):
    try:
        temp=os.getcwd()
        os.makedirs(os.path.join(temp,'sample_'+sample_name))
        os.chdir(os.path.join(temp,'sample_'+sample_name))
        log.debug('creating directory:'+os.getcwd())
    except Exception as e:
        log.exception(e)
    finally:
        return True
