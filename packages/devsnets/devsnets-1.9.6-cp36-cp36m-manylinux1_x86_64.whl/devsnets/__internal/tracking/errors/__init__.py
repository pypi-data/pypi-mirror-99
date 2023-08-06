# import sys
# import atexit
# import platform
# import os

# stderr = None

# class StdErr(object):
#     def __init__(self, tmp_folder):
#         self.stderr = sys.stderr
#         self.tmp_folder = tmp_folder
#         self.is_traceback = False
#         self.error_log = open(os.path.join(self.tmp_folder, 'logs.txt'), 'a+')
#         atexit.register(self.error_log.close)

#     def close_error_log(self):
#         self.error_log.close()
#         atexit.unregister(self.error_log.close)


#     def reopen_error_log(self):
#         self.is_traceback = False
#         self.error_log = open(os.path.join(self.tmp_folder, 'logs.txt'), 'a+')
#         atexit.register(self.error_log.close)


#     def get_error_log_message(self):
#         self.error_log.seek(0)
#         return self.error_log.read()


#     def write(self, error):
#         if not self.is_traceback and 'Traceback' in error:
#             self.is_traceback = True
        
#         if self.is_traceback:
#             try:
#                 self.error_log.write(error)
#                 self.error_log.flush()
#             except:
#                 pass

#         self.stderr.write(error)


# def get_stderr():
#     return stderr


# def init_error_config():
#     global stderr

#     if stderr is None:
#         if platform.system() == 'Windows':
#             system_folder = os.path.join(os.path.expanduser('~'), 'Devsnets', 'system')
#         else:
#             system_folder = os.path.join(os.path.expanduser('~'), 'Devsnets', '.system')
        
#         tmp_folder = os.path.join(system_folder, 'tmp')
#         os.makedirs(tmp_folder, exist_ok=True)

#         sys.stderr = StdErr(tmp_folder)
#         stderr = sys.stderr
        