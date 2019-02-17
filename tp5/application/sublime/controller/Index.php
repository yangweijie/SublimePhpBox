<?php
namespace app\sublime\controller;

use Sublime\Ret;

class Index{

	public function run($call, $args='W10='){
		trace($call);
		trace($args);
		$params = json_decode(base64_decode($args), 1);
		try {
			if(function_exists($call)){
				return call_user_func_array($call, $params);
			}else if(class_exists($call)){
				return call_user_func_array([$call, 'run'], $params);
			}else{
				return Ret::alert("没有{$call}对应的方法或函数");
			}
		} catch (\Exception $e) {
			return Ret::alert($e->getMessage());
		}
	}
}