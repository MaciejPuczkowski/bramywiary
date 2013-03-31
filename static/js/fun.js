function FunSeq( limit, action, classname, data ){
	$(document).ready(function(){
		var button_nr = 0;
		$(classname).live("click",function(){
			if( $(this).hasClass( "" + ( button_nr + 1  ) ) ){
				button_nr += 1;			
				if( button_nr == limit ){
					action(data);
					button_nr = 0;
				}
			}else{
				button_nr = 0;
			}
		});
	});
}

function showFlower( data ){
	var html = "";

	html += "<div class=\"flower\" ><img src=\"" + data["flower"] + "\"  /><div class=\"flower_desc\">" + data["desc"]+ "</div></div>";
	$("body").append( html );
	$(".flower").css({
		position: "fixed",
		width: data["width"],
		height : data["height"],
		left: "600px",
		bottom:0,
		display: "none"
	});
	$(".flower_desc").css({
		zIndex: 1000,
		backgroundColor: "#eee",
		position: "absolute",
		bottom: "0px"
	});
	$(".flower").slideToggle();
	$(".flower").live("click",function(){
		$(this).slideToggle();
		$(this).remove();
	});
}

FunSeq( 6, showFlower , ".funbutton" , { flower: "/static/img/flower.jpg", width: "275px", height: "320px", desc:"Dla Dorotki!" });
