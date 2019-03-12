/**
 * Created by Administrator on 2018/1/10.
 * form by �úú�����
 * email 1570302023@qq.com
 *
 *
 *
 */

$(function () {
    $('.bot-img ul li').click(function () {
        var _this = $(this);
        _this.addClass('active').siblings('li').removeClass('active');
        var int = _this.index();
        $('.activeimg').animate({left: int * -500}, "slow");
    });
    var list = $('.bot-img ul li').length;
    $('.activeimg').css({
        width: list * 500,
    });
    $('.right').click(function () {
        next(list)

    })
    $('.left').click(function () {
        prev(list)
    });

    //�Զ����� 2�벥��һ�� ����ѭ��
    var timer = '';
    var num = 0;
    timer = setInterval(function () { //�򿪶�ʱ��
        num++;
        if (num > parseFloat(list) - 1) {
            num = 0;
            $('.activeimg').animate({left: num * -500}, "slow");
        } else {
            $('.activeimg').animate({left: num * -500}, "slow");
        }
    }, 2000);
})
var index = 0;

//��һ��
function next(list) {
    if (index < list - 1) {
        index++;
        $('.activeimg').animate({left: index * -500}, "slow");
        $('.bot-img ul li').eq(index).addClass('active').siblings('li').removeClass('active')
    } else {
        index = 0;
        $('.activeimg').animate({left: index * -522}, "slow");
        $('.bot-img ul li').eq(index).addClass('active').siblings('li').removeClass('active')
    }
}

//        ��һ��
function prev(list) {
    index--;
    if (index < 0) {
        index = list - 1;
        $('.activeimg').animate({left: index * -500}, "slow");
        $('.bot-img ul li').eq(index).addClass('active').siblings('li').removeClass('active')
    } else {
        $('.activeimg').animate({left: index * -500}, "slow");
        $('.bot-img ul li').eq(index).addClass('active').siblings('li').removeClass('active')
    }
}

jQuery(document).ready(function ($) {

    var jssor_1_SlideshowTransitions = [
        {
            $Duration: 1200,
            x: 0.3,
            $During: {$Left: [0.3, 0.7]},
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: -0.3,
            $SlideOut: true,
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: -0.3,
            $During: {$Left: [0.3, 0.7]},
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: 0.3,
            $SlideOut: true,
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: 0.3,
            $During: {$Top: [0.3, 0.7]},
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: -0.3,
            $SlideOut: true,
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: -0.3,
            $During: {$Top: [0.3, 0.7]},
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: 0.3,
            $SlideOut: true,
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: 0.3,
            $Cols: 2,
            $During: {$Left: [0.3, 0.7]},
            $ChessMode: {$Column: 3},
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: 0.3,
            $Cols: 2,
            $SlideOut: true,
            $ChessMode: {$Column: 3},
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: 0.3,
            $Rows: 2,
            $During: {$Top: [0.3, 0.7]},
            $ChessMode: {$Row: 12},
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: 0.3,
            $Rows: 2,
            $SlideOut: true,
            $ChessMode: {$Row: 12},
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: 0.3,
            $Cols: 2,
            $During: {$Top: [0.3, 0.7]},
            $ChessMode: {$Column: 12},
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            y: -0.3,
            $Cols: 2,
            $SlideOut: true,
            $ChessMode: {$Column: 12},
            $Easing: {$Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: 0.3,
            $Rows: 2,
            $During: {$Left: [0.3, 0.7]},
            $ChessMode: {$Row: 3},
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: -0.3,
            $Rows: 2,
            $SlideOut: true,
            $ChessMode: {$Row: 3},
            $Easing: {$Left: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: 0.3,
            y: 0.3,
            $Cols: 2,
            $Rows: 2,
            $During: {$Left: [0.3, 0.7], $Top: [0.3, 0.7]},
            $ChessMode: {$Column: 3, $Row: 12},
            $Easing: {$Left: $Jease$.$InCubic, $Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            x: 0.3,
            y: 0.3,
            $Cols: 2,
            $Rows: 2,
            $During: {$Left: [0.3, 0.7], $Top: [0.3, 0.7]},
            $SlideOut: true,
            $ChessMode: {$Column: 3, $Row: 12},
            $Easing: {$Left: $Jease$.$InCubic, $Top: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            $Delay: 20,
            $Clip: 3,
            $Assembly: 260,
            $Easing: {$Clip: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            $Delay: 20,
            $Clip: 3,
            $SlideOut: true,
            $Assembly: 260,
            $Easing: {$Clip: $Jease$.$OutCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            $Delay: 20,
            $Clip: 12,
            $Assembly: 260,
            $Easing: {$Clip: $Jease$.$InCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        },
        {
            $Duration: 1200,
            $Delay: 20,
            $Clip: 12,
            $SlideOut: true,
            $Assembly: 260,
            $Easing: {$Clip: $Jease$.$OutCubic, $Opacity: $Jease$.$Linear},
            $Opacity: 2
        }
    ];

    var jssor_1_options = {
        $AutoPlay: true,
        $SlideshowOptions: {
            $Class: $JssorSlideshowRunner$,
            $Transitions: jssor_1_SlideshowTransitions,
            $TransitionsOrder: 1
        },
        $ArrowNavigatorOptions: {
            $Class: $JssorArrowNavigator$
        },
        $ThumbnailNavigatorOptions: {
            $Class: $JssorThumbnailNavigator$,
            $Cols: 10,
            $SpacingX: 8,
            $SpacingY: 8,
            $Align: 360
        }
    };

    var jssor_1_slider = new $JssorSlider$("jssor_1", jssor_1_options);

    /*responsive code begin*/

    /*you can remove responsive code if you don't want the slider scales while window resizing*/
    function ScaleSlider() {
        var refSize = jssor_1_slider.$Elmt.parentNode.clientWidth;
        if (refSize) {
            refSize = Math.min(refSize, 800);
            jssor_1_slider.$ScaleWidth(refSize);
        }
        else {
            window.setTimeout(ScaleSlider, 30);
        }
    }

    ScaleSlider();
    $(window).bind("load", ScaleSlider);
    $(window).bind("resize", ScaleSlider);
    $(window).bind("orientationchange", ScaleSlider);
    /*responsive code end*/
});

$(".topimg1").hover(function () {
    $(".topimg1").css("transform", "scale(1.2)");
    $(".topp1").css("transform", "scale(1.2)");
    $(".topp1").css("color", "red");
}, (function () {
    $(".topimg1").css("transform", "scale(0.8)");
    $(".topp1").css("transform", "scale(0.8)");
    $(".topimg1").css("transform", "scale(1)");
    $(".topp1").css("transform", "scale(1)");
    $(".topp1").css("color", "black");
}))


$(".topimg2").hover(function () {
    $(".topimg2").css("transform", "scale(1.2)");
    $(".topp2").css("transform", "scale(1.2)");
    $(".topp2").css("color", "red");
}, (function () {
    $(".topimg2").css("transform", "scale(0.8)");
    $(".topp2").css("transform", "scale(0.8)");
    $(".topimg2").css("transform", "scale(1)");
    $(".topp2").css("transform", "scale(1)");
    $(".topp2").css("color", "black");
}))
$(".topimg3").hover(function () {
    $(".topimg3").css("transform", "scale(1.2)");
    $(".topp3").css("transform", "scale(1.2)");
}, (function () {
    $(".topimg3").css("transform", "scale(0.8)");
    $(".topp3").css("transform", "scale(0.8)");
    $(".topimg3").css("transform", "scale(1)");
    $(".topp3").css("transform", "scale(1)");
    $(".topp3").css("color", "black");
}))
$(".topimg4").hover(function () {
    $(".topimg4").css("transform", "scale(1.2)");
    $(".topp4").css("transform", "scale(1.2)");
    $(".topp4").css("color", "red");
}, (function () {
    $(".topimg4").css("transform", "scale(0.8)");
    $(".topp4").css("transform", "scale(0.8)");
    $(".topimg4").css("transform", "scale(1)");
    $(".topp4").css("transform", "scale(1)");
    $(".topp4").css("color", "black");
}))
$(".topimg5").hover(function () {
    $(".topimg5").css("transform", "scale(1.2)");
    $(".topp5").css("transform", "scale(1.2)");
    $(".topp5").css("color", "red");
}, (function () {
    $(".topimg5").css("transform", "scale(0.8)");
    $(".topp5").css("transform", "scale(0.8)");
    $(".topimg5").css("transform", "scale(1)");
    $(".topp5").css("transform", "scale(1)");
    $(".topp5").css("color", "black");
}))
$(".topimg6").hover(function () {
    $(".topimg6").css("transform", "scale(1.2)");
    $(".topp6").css("transform", "scale(1.2)");
    $(".topp6").css("color", "red");
}, (function () {
    $(".topimg6").css("transform", "scale(0.8)");
    $(".topp6").css("transform", "scale(0.8)");
    $(".topimg6").css("transform", "scale(1)");
    $(".topp6").css("transform", "scale(1)");
    $(".topp6").css("color", "black");
}))
$(".topimg7").hover(function () {
    $(".topimg7").css("transform", "scale(1.2)");
    $(".topp7").css("transform", "scale(1.2)");
    $(".topp7").css("color", "red");
}, (function () {
    $(".topimg7").css("transform", "scale(0.8)");
    $(".topp7").css("transform", "scale(0.8)");
    $(".topimg7").css("transform", "scale(1)");
    $(".topp7").css("transform", "scale(1)");
    $(".topp7").css("color", "black");
}))
$(".topimg8").hover(function () {
    $(".topimg8").css("transform", "scale(1.2)");
    $(".topp8").css("transform", "scale(1.2)");
    $(".topp8").css("color", "red");
}, (function () {
    $(".topimg8").css("transform", "scale(0.8)");
    $(".topp8").css("transform", "scale(0.8)");
    $(".topimg8").css("transform", "scale(1)");
    $(".topp8").css("transform", "scale(1)");
    $(".topp8").css("color", "black");
}))

$(".topimg9").hover(function () {
    $(".topimg9").css("transform", "scale(1.2)");
    $(".topp9").css("transform", "scale(1.2)");
    $(".topp9").css("color", "red");
}, (function () {
    $(".topimg9").css("transform", "scale(0.8)");
    $(".topp9").css("transform", "scale(0.8)");
    $(".topimg9").css("transform", "scale(1)");
    $(".topp9").css("transform", "scale(1)");
    $(".topp9").css("color", "black");
}))
$(".topimg10").hover(function () {
    $(".topimg10").css("transform", "scale(1.2)");
    $(".topp10").css("transform", "scale(1.2)");
    $(".topp10").css("color", "red");
}, (function () {
    $(".topimg10").css("transform", "scale(0.8)");
    $(".topp10").css("transform", "scale(0.8)");
    $(".topimg10").css("transform", "scale(1)");
    $(".topp10").css("transform", "scale(1)");
    $(".topp10").css("color", "black");
}))
$(".topimg11").hover(function () {
    $(".topimg11").css("transform", "scale(1.2)");
    $(".topp11").css("transform", "scale(1.2)");
    $(".topp11").css("color", "red");
}, (function () {
    $(".topimg11").css("transform", "scale(0.8)");
    $(".topp11").css("transform", "scale(0.8)");
    $(".topimg11").css("transform", "scale(1)");
    $(".topp11").css("transform", "scale(1)");
    $(".topp11").css("color", "black");
}))
$(".topimg12").hover(function () {
    $(".topimg12").css("transform", "scale(1.2)");
    $(".topp12").css("transform", "scale(1.2)");
    $(".topp12").css("color", "red");
}, (function () {
    $(".topimg12").css("transform", "scale(0.8)");
    $(".topp12").css("transform", "scale(0.8)");
    $(".topimg12").css("transform", "scale(1)");
    $(".topp12").css("transform", "scale(1)");
    $(".topp12").css("color", "black");
}))
$(".topimg13").hover(function () {
    $(".topimg13").css("transform", "scale(1.2)");
    $(".topp13").css("transform", "scale(1.2)");
    $(".topp13").css("color", "red");
}, (function () {
    $(".topimg13").css("transform", "scale(0.8)");
    $(".topp13").css("transform", "scale(0.8)");
    $(".topimg13").css("transform", "scale(1)");
    $(".topp13").css("transform", "scale(1)");
    $(".topp13").css("color", "black");
}))
$(".topimg14").hover(function () {
    $(".topimg14").css("transform", "scale(1.2)");
    $(".topp14").css("transform", "scale(1.2)");
    $(".topp14").css("color", "red");
}, (function () {
    $(".topimg14").css("transform", "scale(0.8)");
    $(".topp14").css("transform", "scale(0.8)");
    $(".topimg14").css("transform", "scale(1)");
    $(".topp14").css("transform", "scale(1)");
    $(".topp14").css("color", "black");
}))

(function ($) {

    $.fn.myScroll = function (options) {
        //默认配置
        var defaults = {
            speed: 40,  //滚动速度,值越大速度越慢
            rowHeight: 24 //每行的高度
        };

        var opts = $.extend({}, defaults, options), intId = [];

        function marquee(obj, step) {

            obj.find("ul").animate({
                marginTop: '-=1'
            }, 0, function () {
                var s = Math.abs(parseInt($(this).css("margin-top")));
                if (s >= step) {
                    $(this).find("li").slice(0, 1).appendTo($(this));
                    $(this).css("margin-top", 0);
                }
            });
        }

        this.each(function (i) {
            var sh = opts["rowHeight"], speed = opts["speed"], _this = $(this);
            intId[i] = setInterval(function () {
                if (_this.find("ul").height() <= _this.height()) {
                    clearInterval(intId[i]);
                } else {
                    marquee(_this, sh);
                }
            }, speed);

            _this.hover(function () {
                clearInterval(intId[i]);
            }, function () {
                intId[i] = setInterval(function () {
                    if (_this.find("ul").height() <= _this.height()) {
                        clearInterval(intId[i]);
                    } else {
                        marquee(_this, sh);
                    }
                }, speed);
            });

        });

    }

})(jQuery);

$(function () {

    $("div.ranklist").myScroll({
        speed: 40,
        rowHeight: 24
    });

});
