var t = '1'

function test(x) {
    if (x == '1' && t == '1') {
        document.getElementById(x).style.color = 'red'
    }
    else if (x != t) {
        document.getElementById(x).style.color = 'red'
        document.getElementById(t).style.color = '#a6a6a6'
        t = x
    }
}

$(function () {
    $("#nav li").click(function () {
        $("#nav li").eq($(this).index()).addClass("rt1").siblings().removeClass("rt1");
    })
})


$(function () {
    $(".rty li").click(function () {
        $(".rty li").eq($(this).index()).addClass("current").siblings().removeClass("current");
    })
})

$(document).ready(function () {
    $("#shop1").click(function () {
        $(".shopping").show()
        $(".read").hide()

    });
});

$(document).ready(function () {
    $("#shop2").click(function () {
        $(".read").show()
        $(".shopping").hide()

    })

})
$(document).ready(function () {

        $(".shopping").show()
        $(".read").hide()



})


function goToPage(type,state,shuxing,word) {
    value=$("#jumppage").val()
    if(value>3){
        value=3
    }
    location.href = "?type=" + type + "&state=" + state + "&shuxing=" + shuxing + "&word=" + word + "&page=" + value;
}

$(document).ready(function () {
    a = $(".all-img-list-cf").children()
    if (a.length == 0) {
        $("#backimg").show()
        $(".book-img-text").hide()
    }

})