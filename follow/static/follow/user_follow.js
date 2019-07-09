
    $(document).ready(function(){
        $('#follow_user').click(function(e){
            e.preventDefault();
        // followers number and follow/unfollow variable
        var follow_count = $('#follower_count').text();
        var follow_count_conv = parseInt(follow_count);
        var data_url = $(this).attr('data_url');


        $.ajax({
            url: data_url,
            success: function(data){
                if (data.follower_add){
                    $('#follow_status').text('Following');
                    $('#follower_count').text(follow_count_conv + 1);
                    console.log("{% url 'user_follow' user_info.pk %}");
                }
                else{
                    $('#follow_status').text('Follow');
                    if (follow_count_conv > 0){
                        $('#follower_count').text(follow_count_conv -1);

                    }
                }
            },
            error: function(){
                $('#alert_messg').text('Not successful');

            }

        })

        })
    })