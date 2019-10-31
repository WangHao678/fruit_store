window.onload = function (){
	/*-----------下拉菜单---------*/
	//1. 获取元素节点
	var currentAddr = document.getElementsByClassName('currentAddress')[0];
	var select = document.getElementsByClassName('select')[0];
	//获取内层列表中地址项
	var address = select.children;
	//为每一项添加点击事件
	for(var i = 0; i < address.length; i ++){
		address[i].onclick = function(){
			//传值
			currentAddr.innerHTML = this.innerHTML;
		};
	}
	/*-----------图片轮播-----------*/
	//1. 获取图片数组
	//2. 定时器实现图片切换
	//3. 图片切换主要切换数组下标，防止数组越界
	var banner = document.getElementsByClassName('wrapper')[0];
	var imgs = banner.children; //图片数组
	var imgNav = document.getElementsByClassName('imgNav')[0];
	var indInfo = imgNav.children; //索引数组
	var imgIndex = 0; //初始下标
	var timer;
	timer = setInterval(autoPlay,1000); //定时器
	function autoPlay(){
		//设置元素隐藏与显示
		imgs[imgIndex].style.display = "none";
		/*
		++ imgIndex;
		if(imgIndex == imgs.length){
			imgIndex = 0;
		}
		*/
		imgIndex = ++ imgIndex == imgs.length ? 0 : imgIndex;
		imgs[imgIndex].style.display = "block";
		for(var i = 0; i < indInfo.length; i ++){
			indInfo[i].style.background = "gray";
		}
		//切换索引 切换背景色
		indInfo[imgIndex].style.background = "red";
	}
	banner.onmouseover = function (){
		//停止定时器
		clearInterval(timer);
	};
	banner.onmouseout = function (){
		timer = setInterval(autoPlay,1000);
	};
};


//检查用户登录状态
function check_login(){
    //向后台发异步请求
    $.get('/index/check_login',function(data){
        var html = '';
        //{loginState:0}
        if (data.loginState == 0){
            html = "<a href='/index/login'>[登录]</a>";
            html += "<a href='/index/register'>[注册,有惊喜]</a>";
        }else{
            //{'loginState':1,'username':'wang..'}
            html += "欢迎:" + data.username;
            html += "<a href='/index/logout'>退出</a>";
        }
        $("#login").html(html)
    },'json');
}




function loadGoods(){
    $.get('/index/load_goods',function(data){
        //[{'type':{'title':xxx},'goos':[{'title':xx,}]},...]
        var show = '';
        $.each(data,function(i,obj){
            show += '<div class="title">';
                show += '<h3 class="fl">' + obj.type.title+'</h3>';
                show += '<div class="fr">更多</div>';
                show += '<div class="cb"></div>';
            show += '</div>';
            //记得封口
            show += '<ul>';
            $.each(obj.goods,function(ix,gobj){
                //循环商品 生成 li 区域
                show += '<li class="fl">';
                    show += '<div class="box">';
                        show += '<figure>';
                            show += '<img src="/'+ gobj.picture + '">';
                        show += '</figure>';
                        show += '<div class="tip">';
                            show += '<div class="fl">';
                                show += '<h4>' + gobj.title +'</h4>';
                                show += '<p>$' + gobj.price + '/' + gobj.spec + '</p>';
                            show += '</div>';
                            show += '<div class="fr">';
                                show += '<figure>';
                                    show += '<img src="/static/upload/goods/images/cart.png">';
                                show += '</figure>';
                            show += '</div>';
                            show += '<div class="cb"></div>';
                        show += '</div>';
                    show += '</div>';
                show += '</li>';

            });
            show += '</ul>';
        });
        $('#main').html(show);
    },'json');
}



$(function(){
    //1.check_login
    check_login();
    //2.load_goods
    loadGoods();

})









