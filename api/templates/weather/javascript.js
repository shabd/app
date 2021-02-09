

    $(document).on('submit','#form',function(e){
        // prevent page refresh 
        e.preventDefault();


        $.ajax({
        type:'POST',
            url: '/api/weather',
            data:{
                 name:$('#name').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(){
        aleart("sent");
            }

        })
   });





 function historical_weather() {
        //  var cityname ='{{weather}';
        $.ajax({
            type: "GET",
            data: {
                weather_name: name,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            url: "api/historical_weather",
            success: function (data) {
                alert("Hi I am former " + data.name + " and I came from Django");

            }

        });


