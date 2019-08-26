
$(document).ready(
    function thumpUP(){
        $('.thump_up_post').click(function(){
            // extract the url
            var url = $(this).attr('post_thump_up_url');
            var thump_up_count = $('#thump_up_count').text();
            var parseThumpUpCount = parseInt(thump_up_count);
            var thump_down_count = $('#thump_down_count').text();
            var parseThumpDownCount = parseInt(thump_down_count);
            var upCount;

            $.ajax({
                type: 'get',
                url: url,
                success: function(data){
                    if (data.added){
                        console.log(data.added);
                        // check if user has never thumped up, then add to count
                        // and minus the thumped down
                        upCount = parseThumpUpCount +1;
                        $('#thump_up_count').text(upCount);
                        if (data.already_thumped_down && thump_down_count > 0){
                            $('#thump_down_count').text(parseThumpDownCount -= 1);
                        }
                    }else{
                        upCount = parseThumpUpCount -1;
                        $('#thump_up_count').text(upCount);
                    }
                },
                error: function(){
                    // notify the user in the frontend!!!

                }

            });
            

        });

    })

    $(document).ready(
        function thumDown(){
            $('.thump_down_post').click(function(e){
                e.preventDefault();
                // extract the url
                var url = $(this).attr('thump_down_url');
                var thump_down_count = $('#thump_down_count').text();
                var parseThumpDownCount = parseInt(thump_down_count);
                var thump_up_count = $('#thump_up_count').text();
                var parseThumpUpCount = parseInt(thump_up_count);
    
                $.ajax({
                    type: 'get',
                    url: url,
                    success: function(data){
                        if (data.added){
                            // check if user has never thumped up, then add to count
                            // and minus the thumped down
                            $('#thump_down_count').text(parseThumpDownCount += 1);
                            if (data.already_thumped_up && thump_up_count >= 0){
                                $('#thump_up_count').text(parseThumpUpCount - 1);
                            }
                        }else{
                            $('#thump_down_count').text(parseThumpDownCount -= 1);
                        }
                    },
                    error: function(){
                        // notify the user in the frontend!!!
    
                    }
    
                });
        });
    }
    )


$(document).ready(
// ajax call for following post
function followPost(){
    $('#follow').click(function(e){
        e.preventDefault();
        var followText = $('#follow').text();
        var url = $(this).attr('followUrl');

    $.ajax({
        type: 'get',
        url: url,
        success: function(data){
            if (data.added){
                if (followText === 'Follow Thread'){
                    $('#follow').text('Following Thread')
                }
                
            }else{
                if (followText === 'Following Thread'){
                    $('#follow').text('Follow Thread')
                }
            }
        },
        error: function(){
            // the logic will be done with frontend later!!!
        }
    });


    })
}
)