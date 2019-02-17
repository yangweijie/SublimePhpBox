# -*- coding: utf-8 -*-
import sublime, sublime_plugin, sys
# import sublime_lib
import os, subprocess, string, json, threading, re, time
import base64

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

class php_execute(threading.Thread):
	def __init__(self, cmd, args):
		self.cmd = cmd
		self.args = args
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
						self.window.run_command(u"{0}".format(result['on_done_cmd']['cmd']), result['on_done_cmd']['args'])
				def on_quick_highlighted(index):
					if result['on_highlighted_cmd'] == []:
						pass
					else:
						# result.args 合并 index
						self.window.run_command(u"{0}".format(result['on_highlighted_cmd']['cmd']), result['on_highlighted_cmd']['args'])
			elif result['type'] == 'show_input_panel':
				def on_input_done(str):
					if result['on_done_cmd'] == []:
						pass
					else:
						# result.args 合并 str
						self.window.run_command(u"{0}".format(result['on_done_cmd']['cmd']), result['on_done_cmd']['args'])
				def on_input_change(str):
					if result.on_change_cmd == []:
						pass
					else:
						# result['args'] 合并 str
						self.window.run_command(u"{0}".format(result.on_change_cmd['cmd']), result.on_change_cmd['args'])
				def on_input_cancel():
					if result.on_change_cmd == []:
						pass
					else:
						self.window.run_command(u"{0}".format(result.on_cancel_cmd['cmd']), result.on_cancel_cmd['args'])
				ret = self.view.show_input_panel(u"{0}".format(result.caption), u"{0}".format(result.initial_text), on_input_done, on_input_change, on_input_cancel)
		else:
			sublime.error_message(u"{0}".format(result['msg']))

class PhpBoxCommand(sublime_plugin.TextCommand):
	def run(self, edit, call, cmd_args):
		self.setting = sublime.load_settings("PhpBox.sublime-settings")
		print(command_bin)

		thread = php_execute('test_yes', {'msg':'好123', 'ok_title':'确认'})
		thread.start()
		ThreadProgress(thread, 'Is excuting', 'Finding Done')



# thread = UpgradeAllPackagesThread(self.window, package_renamer)
#         thread.start()
#         ThreadProgress(thread, 'Loading repositories', '')


