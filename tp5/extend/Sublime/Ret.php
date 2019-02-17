<?php
namespace Sublime;

class Ret{
	const RETURN_TYPE_ALERT             = 'error_dialog';
	const RETURN_TYPE_MSG               = 'msg_dialog';
	const RETURN_TYPE_OK                = 'ok_cancel_dialog';
	const RETURN_TYPE_YES               = 'yes_no_cancel_dialog';
	const RETURN_TYPE_CMD_SET_CLIPBOARD = 'set_clipboard';
	const RETURN_TYPE_CMD_RUN_COMMAND   = 'run_command';
	const RETURN_TYPE_SHOW_QUICK_PANEL  = 'show_quick_panel';
	const RETURN_TYPE_SHOW_INPUT_PANEL  = 'show_input_panel';

	const SUBLIMT_CONSTS = [
		'MONOSPACE_FONT'          => 1,
		'KEEP_OPEN_ON_FOCUS_LOST' => 2,
	];

	public static function alert($msg, $cmd=''){
		$arr = [
			'code' => 404,
			'type' => self::RETURN_TYPE_ALERT,
			'msg'  => $msg,
		];
		return self::encode($arr);
	}

	public static function msg($msg){
		$arr = [
			'code'  => 200,
			'type'  => self::RETURN_TYPE_MSG,
			'msg'   => $msg,
		];
		return self::encode($arr);
	}

	public static function ok($msg, $ok_title='', $ok_cmd=[]){
		$arr = [
			'code'     => 200,
			'type'     => self::RETURN_TYPE_OK,
			'msg'      => $msg,
			'ok_title' => $ok_title,
			'ok_cmd'   => $ok_cmd,
		];
		return self::encode($arr);
	}

	public static function yes($msg, $yes_title, $no_title, $yes_cmd=[], $no_cmd=[], $cancel_cmd =[]){
		$arr = [
			'code'       => 200,
			'type'       => self::RETURN_TYPE_YES,
			'msg'        => $msg,
			'yes_title'  => $yes_title,
			'yes_cmd'    => $yes_cmd,
			'no_title'   => $no_title,
			'no_cmd'     => $no_cmd,
			'cancel_cmd' => $cancel_cmd,
		];
		return self::encode($arr);
	}

	public static function set_clipboard($str){
		$arr = [
			'code'  => 200,
			'type'  => self::RETURN_TYPE_CMD_SET_CLIPBOARD,
			'str'   => $str,
		];
		return self::encode($arr);
	}

	/**
	 * [show_quick_panel]
	 * @param  array   $items     字符串数组或者键值数组
	 * @param  array   $on_done_cmd  选择结束命令 cmd 和args
	 * @param  int     $flag  sublime.MONOSPACE_FONT 或 KEEP_OPEN_ON_FOCUS_LOST
	 * @param  integer $selected_index     选中的list 的index
	 * @param  array   $on_highlighted_cmd 高亮命令
	 * @return string
	 */
	public static function show_quick_panel($items, $on_done_cmd = [], $flag, $selected_index = -1, $on_highlighted_cmd = []){
		$arr = [
			'code'               => 200,
			'type'               => self::RETURN_TYPE_SHOW_QUICK_PANEL,
			'items'              => $items,
			'on_done_cmd'        => $on_done_cmd,
			'flag'               => $flag,
			'on_highlighted_cmd' => $on_highlighted_cmd,
		];
		return self::encode($arr);
	}

	public static function show_input_panel($caption, $initial_text = '', $on_done_cmd = [], $on_change_cmd = [], $on_cancel_cmd = []){
		$arr = [
			'code'          => 200,
			'type'          => self::RETURN_TYPE_SHOW_INPUT_PANEL,
			'caption'       => $caption,
			'initial_text'  => $initial_text,
			'on_done_cmd'   => $on_done_cmd,
			'on_change_cmd' => $on_change_cmd,
			'on_cancel_cmd' => $on_cancel_cmd,
		];
		return self::encode($arr);
	}

	public static function run_command($cmd, $args=[]){
		$arr = [
			'code' => 200,
			'type' => self::RETURN_TYPE_CMD_RUN_COMMAND,
			'cmd'  => $cmd,
			'args' => $args,
		];
		return self::encode($arr);
	}

	public static function encode($arr){
		return base64_encode(json_encode($arr, JSON_UNESCAPED_UNICODE));
	}

	public static function decode($str){
		return json_decode(base64_decode($str), true);
	}
}