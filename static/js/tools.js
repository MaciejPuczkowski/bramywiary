$(document).ready(function(){
	$("a.hdesc").click(function(){
		$(this).next().slideToggle( 100 );
		return false;
	});
	$(".sentence").load($(".sentence").find("a").attr("href"), function(){
		$(".sentence").find(".stext").fadeToggle( 300 );
		var text = $(".sentence").find(".stext");
		var fsize =  text.css("fontSize").substring( 0, text.css("fontSize").length -2 );
		while( text.height() > $(".sentence").height() ){
			fsize = fsize * 0.9;
			text.css("fontSize", fsize  + "px" );
		}
		var top = (  $(".sentence").height() - text.height() ) / 2;
		text.css( "marginTop", top + "px");
	});
	
	setInterval(function(){
		$(".sentence").find(".stext").fadeToggle( 300 );
		setTimeout( function(){
			$(".sentence").load($(".sentence").find("a").attr("href"), function(  ){
				
				$(".sentence").find(".stext").fadeToggle( 300 );
				var text = $(".sentence").find(".stext");
				var fsize =  text.css("fontSize").substring( 0, text.css("fontSize").length -2 );
				while( text.height() > $(".sentence").height() ){
					fsize = fsize * 0.9;
					text.css("fontSize", fsize  + "px" );
				}
				var text = $(".sentence").find(".stext");
				var top = (  $(".sentence").height() - text.height() ) / 2;
				text.css( "marginTop", top + "px");
			});
			
		} , 300 );
		
	},
		30000
	);
	var g_width = 0;
	
	$("#sponsor .container").load( $("#sponsor ").find("a").attr("href"), function(){
		console.log($(".flash_sponsor").last().outerWidth());
		 
		if( $(".flash_sponsor").length > 1 ){
			setInterval(function(){
				
				e = $(".flash_sponsor").last().clone();
				$(".flash_sponsor").last().remove();
				$(".container").prepend( e  );
				$(".flash_sponsor").first().toggle();
				$(".flash_sponsor").first().fadeToggle();
				
			}, 3000 );
		}
		
	} );
	var left = $(".colorbox .subheader .title").css( "left" );
	left = parseInt( left )
	var top_ = $(".colorbox .subheader .title").css( "top" );
	
	top_ = parseInt( top_ );
	//alert( top_ );
	$(".colorbox .subcontent.dynamic").css({
		marginLeft: parseInt( left ) + 5 + $(".colorbox .subheader .title").width() + "px",
		marginTop: parseInt( top_ ) + 5 + $(".colorbox .subheader .title").height() + "px"
	});
	
});