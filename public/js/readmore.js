
$(function(){ /* to make sure the script runs after page load */

	$(".more_text").css("display", "none");
    

	$('.item').each(function(event){ /* select all divs with the item class */

			$(this).find('a.read_more').click(function(event){ /* find the a.read_more element within the new html and bind the following code to it */
 
				event.preventDefault(); /* prevent the a from changing the url */
				$(this).hide(); /* hide the read more button */
				$(this).parents('.item').find('.more_text').show(); /* show the .more_text span */
		 
			});
	});
}); 