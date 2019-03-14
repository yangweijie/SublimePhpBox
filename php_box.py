# -*- coding: utf-8 -*-
import sublime, sublime_plugin, sys
# import sublime_lib
import os, subprocess, string, json, threading, re, time
import base64,binascii

from .thread_progress import ThreadProgress

package_name = 'PhpBox'
packages_path = os.path.split(os.path.realpath(__file__))[0]
command_bin = packages_path + os.sep + 'tp5' + os.sep + 'public' + os.sep + 'index.php'

def PKGPATH():
	return os.path.join(sublime.packages_path(), "PhpBox")
def CMD_DIR():
	return os.path.join(ChigiArgs.PKGPATH(), 'sublime_php_command')
def CMD_PATH():
	return os.path.join(ChigiArgs.CMD_DIR(), 'sublime.php')

def plugin_loaded():
	from package_control import events

	if events.install(package_name):
		print('in loader')
		thread = check_php_bin()
		thread.start()
		ThreadProgress(thread, 'Is excuting', 'Finding Done')
	elif events.post_upgrade(package_name):
		print('Upgraded to %s!' % events.post_upgrade(package_name))

class php_execute(threading.Thread):
	def __init__(self, cmd, args, view, window):
		self.cmd = cmd
		self.args = args
		self.view = view
		self.window = window
		global command_bin
		self.php_bin = command_bin
		threading.Thread.__init__(self)

	def run(self):

		command_text = 'php "' + command_bin + '" sublime/index/run/call/'+self.cmd+'/args/'+ base64.b64encode(json.dumps(self.args, sort_keys=True).encode('utf-8')).decode('utf-8')
		print(command_text)
		cloums = os.popen(command_text)
		data = cloums.read()
		print(data)
		self.parse_php_result(data)

	def parse_php_result(self, out):
		try:
			print(out)
			result_str_raw = out
			# out = out.decode("UTF-8")
		except UnicodeDecodeError as e:
			print(out)
		try:
			result_str = base64.b64decode(out)
		except (TypeError):
			print(out)
			pass
		except (binascii.Error):
			print(out)
			pass
		result = 0;
		try:
			result = json.loads(result_str.decode('utf-8'))
		except (ValueError):
			print('The return value for the php plugin is wrong JSON.',True)
			if len(result_str) > 0:
				try:
					sublime.error_message(u"PHP ERROR:\n{0}".format(result_str.decode('utf-8')))
				except(UnicodeDecodeError):
					sublime.error_message(u"PHP ERROR:\n{0}".format(result_str_raw))
			pass
		print(type(result))
		print(result)
		# -------------------------------------------------------------------
		#                 PHP 通信完成，开始处理结果
		# -------------------------------------------------------------------
		self.executeReceive(result)

	def executeReceive(self, result):
		if result['code'] == 200:
			if result['type'] == 'error_dialog':
				sublime.error_message(u"{0}".format(result['msg']))
			elif result['type'] == 'msg_dialog':
				sublime.message_dialog(u"{0}".format(result['msg']))
			elif result['type'] == 'ok_cancel_dialog':
				ret = sublime.ok_cancel_dialog(u"{0}".format(result['msg']), u"{0}".format(result['ok_title']))
				if ret is True:
					if result['ok_cmd'] != []:
						self.executeReceive(result['ok_cmd'])
			elif result['type'] == 'yes_no_cancel_dialog':
				ret = sublime.yes_no_cancel_dialog(u"{0}".format(result['msg']), u"{0}".format(result['yes_title']), u"{0}".format(result['no_title']))
				if ret == sublime.DIALOG_CANCEL:
					pass
				elif ret == sublime.DIALOG_YES:
					if result['yes_cmd'] != []:
						self.executeReceive(result['yes_cmd'])
				elif ret == sublime.DIALOG_NO:
					if result['no_cmd'] != []:
						self.executeReceive(result['no_cmd'])
			elif result['type'] == 'status_message':
				sublime.status_message(u"{0}".format(result['msg']));
			elif result['type'] == 'set_clipboard':
				ret = sublime.set_clipboard(u"{0}".format(result['str']))
			elif result['type'] == 'run_command':
				self.window.run_command(u"{0}".format(result['cmd']), result['args'])
			elif result['type'] == 'show_quick_panel':
				def on_quick_done(index):
					if result['on_done_cmd'] == []:
						pass
					else:
						# result.args 合并 index
						print(index)
						if 'cmd_args' in result['on_done_cmd']['args']:
							result['on_done_cmd']['args']['cmd_args']['index'] = index
						else:
							result['on_done_cmd']['args']['index'] = index
						print(result['on_done_cmd']['args'])
						self.window.run_command(u"{0}".format(result['on_done_cmd']['cmd']), result['on_done_cmd']['args'])
				def on_quick_highlighted(index):
					if result['on_highlighted_cmd'] == []:
						pass
					else:
						# result.args 合并 index
						print(index)
						if 'cmd_args' in result['on_highlighted_cmd']['args']:
							result['on_highlighted_cmd']['args']['cmd_args']['index'] = index
						else:
							result['on_highlighted_cmd']['args']['index'] = index
						print(result['on_highlighted_cmd']['args'])
						self.window.run_command(u"{0}".format(result['on_highlighted_cmd']['cmd']), result['on_highlighted_cmd']['args'])
				ret = self.window.show_quick_panel(result['items'], on_quick_done, result['flag'], -1, on_quick_highlighted)
			elif result['type'] == 'show_input_panel':
				def on_input_done(str):
					if result['on_done_cmd'] == []:
						pass
					else:
						# result.args 合并 str
						if 'cmd_args' in result['on_done_cmd']['args']:
							result['on_done_cmd']['args']['cmd_args']['str'] = str
						else:
							result['on_done_cmd']['args']['str'] = str
						print(result['on_done_cmd']['args'])
						self.window.run_command(u"{0}".format(result['on_done_cmd']['cmd']), result['on_done_cmd']['args'])
				def on_input_change(str):
					if result['on_change_cmd'] == []:
						pass
					else:
						# result['args'] 合并 str
						if 'cmd_args' in result['on_change_cmd']['args']:
							result['on_change_cmd']['args']['cmd_args']['str'] = str
						else:
							result['on_change_cmd']['args']['str'] = str
						print(result['on_change_cmd']['args'])
						self.window.run_command(u"{0}".format(result.on_change_cmd['cmd']), result.on_change_cmd['args'])
				def on_input_cancel():
					if result['on_cancel_cmd'] == []:
						pass
					else:
						self.window.run_command(u"{0}".format(result.on_cancel_cmd['cmd']), result.on_cancel_cmd['args'])
				ret = self.window.show_input_panel(u"{0}".format(result.caption), u"{0}".format(result.initial_text), on_input_done, on_input_change, on_input_cancel)
			elif result['type'] == 'run_command':
				cmd = u"{0}".format(result['cmd'])
				if result['from'] == 'window':
					self.window.run_command(cmd, result['args'])
				elif result['from'] == 'view':
					pass
				elif result['from'] == 'applicant':
					sublime.run_command(cmd, result['args'])
		else:
			sublime.error_message(u"{0}".format(result['msg']))

class check_php_bin(threading.Thread):
	def run(self):
        self.settings = sublime.load_settings("PhpBox.sublime-settings")
        self.php_path = self.setting.get("php_path");
    	check_php_path = os.popen(self.php_path + ' -v').read()
        print("3###");
        pattern = re.compile(r'^PHP \d+.\d+');
        if pattern.match(check_php_path):
            check_php_path = True;
        else:
            check_php_path = False;
        if check_php_path == False:
        	sublime.windows()[0].show_input_panel(u'Please input php bin path', '/usr/local/bin', self.done, None, None)
    def done(path):
    	self.settings.set('php_path', path)



class PhpBoxCommand(sublime_plugin.TextCommand):
	def run(self, edit, call, cmd_args):
		self.setting = sublime.load_settings("PhpBox.sublime-settings")
		print(command_bin)
		print(call)
		print(cmd_args)
		if call == '':
			thread = php_execute('app\\sublime\\command\\ListCmd', cmd_args, self.view, sublime.windows()[0])
		else:
			thread = php_execute(call, cmd_args, self.view, sublime.windows()[0])

		# thread = php_execute('test_show_quick_panel', {'items':['a','b','c']}, self.view, sublime.windows()[0])
		# thread = php_execute('test_show_quick_panel', {'items':[['a','a'],['b','b'],['c','c']]}, self.view, sublime.windows()[0])
		thread.start()
		ThreadProgress(thread, 'Is excuting', 'Finding Done')



# thread = UpgradeAllPackagesThread(self.window, package_renamer)
#         thread.start()
#         ThreadProgress(thread, 'Loading repositories', '')


