
$(function(){

  $("#close").click(function(){
		$("#sideNav").css("width","0px");
	})

    $("#open").click(function(){
		$("#sideNav").css("width","300px");
	})

});

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});

$(window).resize(function(){
    
    $('.col').each(function() {
        $(this).height($(this).width());
    });
    });

