$(document).ready(function(){
    $('input[name="start_time"]').change(function(){
        unique_id = this.id.split("_")[1];
        start_val_str = 'input[id="start_'+unique_id+'"]';
        lunch_val_str = 'input[id="lunch_'+unique_id+'"]';
        end_val_str = 'input[id="end_'+unique_id+'"]';
        worked_val_str = 'input[id="worked_'+unique_id+'"]';
        start_val = $(start_val_str).val();
        lunch_val = $(lunch_val_str).val();
        end_val = $(end_val_str).val();
        worked_val = $(worked_val_str).val();

        $.ajax({
                type: 'POST',
                url: '/calculate_time',
                data: JSON.stringify({id: unique_id,
                                    start: start_val,
                                    lunch:lunch_val,
                                    end:end_val,
                                    worked:worked_val}),
                contentType: "application/json",
                dataType: "json",
                success: function(data){
                    data = JSON.parse(data);
                    $(worked_val_str).val(data.worked)
                },
                failure: function () {
                        alert("Failed!");
                },
                dataType: 'html'
        });
    });



    $('input[name="end_time"]').change(function(){
        unique_id = this.id.split("_")[1];
        start_val_str = 'input[id="start_'+unique_id+'"]';
        lunch_val_str = 'input[id="lunch_'+unique_id+'"]';
        end_val_str = 'input[id="end_'+unique_id+'"]';
        worked_val_str = 'input[id="worked_'+unique_id+'"]';
        start_val = $(start_val_str).val();
        lunch_val = $(lunch_val_str).val();
        end_val = $(end_val_str).val();
        worked_val = $(worked_val_str).val();

        $.ajax({
                type: 'POST',
                url: '/calculate_time',
                data: JSON.stringify({id: unique_id,
                                    start: start_val,
                                    lunch:lunch_val,
                                    end:end_val,
                                    worked:worked_val}),
                contentType: "application/json",
                dataType: "json",
                success: function(data){
                    data = JSON.parse(data);
                    $(worked_val_str).val(data.worked)
                },
                failure: function () {
                        alert("Failed!");
                },
                dataType: 'html'
        });
    });

    $('input[name="lunch_duration"]').change(function(){
        unique_id = this.id.split("_")[1];
        start_val_str = 'input[id="start_'+unique_id+'"]';
        lunch_val_str = 'input[id="lunch_'+unique_id+'"]';
        end_val_str = 'input[id="end_'+unique_id+'"]';
        worked_val_str = 'input[id="worked_'+unique_id+'"]';
        start_val = $(start_val_str).val();
        lunch_val = $(lunch_val_str).val();
        end_val = $(end_val_str).val();
        worked_val = $(worked_val_str).val();

        $.ajax({
                type: 'POST',
                url: '/calculate_time',
                data: JSON.stringify({id: unique_id,
                                    start: start_val,
                                    lunch:lunch_val,
                                    end:end_val,
                                    worked:worked_val}),
                contentType: "application/json",
                dataType: "json",
                success: function(data){
                    data = JSON.parse(data);
                    $(worked_val_str).val(data.worked)
                },
                failure: function () {
                        alert("Failed!");
                },
                dataType: 'html'
        });
    });



});