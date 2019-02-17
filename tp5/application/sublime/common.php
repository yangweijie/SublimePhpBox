<?php
use \Sublime\Ret;

function test_alert($msg){
	return Ret::alert($msg);
}

function test_msg($msg){
	return Ret::msg($msg);
}

function test_ok($msg, $ok_title='', $ok_cmd=[]){
	return Ret::ok($msg, $ok_title, $ok_cmd);
}

function test_yes($msg, $yes_title, $no_title, $yes_cmd=[], $no_cmd=[], $cancel_cmd =[]){
	return Ret::yes($msg, $yes_title, $no_title, $yes_cmd, $no_cmd, $cancel_cmd);
}