
$(function(){

  $("#close").click(function(){
		$("#sideNav").css("width","0px");
	})

    $("#open").click(function(){
		$("#sideNav").css("width","300px");
	})




	$('.col-sm').each(function() {
    $(this).height($(this).width());
    });

	$('#select-multiple').select2();
});

$(window).resize(function(){
    // If there are multiple elements with the same class, "main"
    $('.col').each(function() {
        $(this).height($(this).width());
    });
    });


// //select multiple value from input box
// function multiple_selector(#,selected_list,hidden_input){


// 			input_box.keyup(function(e){

// 				var reader			=	input_box.val();
// 				var comma			=	reader.lastIndexOf(",");


// 				if (e.which==188 || $comma!=-1 ) {

// 					var value 			= 	rtrim(reader,",");

// 					selected_list.append('<li class="list-values">'+value+'<i class="fas value-close fa-times"></i></li>');

// 					hidden_input.val(hidden_input.val()+value+",");

// 					input_box.val('');
// 							}
// 				});

// 		// Input multiple Box on delete 
// 		$(document).on("click", ".value-close", function() {
// 			var remove_from		=	hidden_input;
// 			var to_remove		=	$(this).parent().text();
// 		   	var to_replace		=	remove_from.val();
// 		    var replaced		=	to_replace.replace(to_remove+",","");   

// 			remove_from.val(replaced);

// 		   	$(this).parent().remove();
// 		});
// }

// multiple_selector($("#sub-selector"),$("#sub-values-list ul"),$("#hidden-sub"));
