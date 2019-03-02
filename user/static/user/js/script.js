
$(function(){

  $("#close").click(function(){
		$("#sideNav").css("width","0px");
	})

    $("#open").click(function(){
		$("#sideNav").css("width","300px");
	})

});

$(window).resize(function(){
    
    $('.col').each(function() {
        $(this).height($(this).width());
    });
    });

