
$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	var actions = $("table td:last-child").html();
	// Append table with add row form on add new button click
    $(".add-new").click(function(){
		$(this).attr("disabled", "disabled");
		var index = $("table tbody tr:last-child").index();
        var row = 
        	'<tr>' + '<form method="POST" action="/admin/teacher_manage">'+
            '<td><input type="text" class="form-control" name="username" id="name"></td>' +
            '<td><input type="text" class="form-control" name="department" id="department"></td>' +
            '<td><input type="text" class="form-control" name="password" id="phone"></td>' +
			'<td>' + actions + '</td>' +
			'<a class="add" type="submit" title="" data-toggle="tooltip" data-original-title="Add" style="display: inline;"><i class="fa fa-user-plus" style="width: 20px; height: 20px;"></i></a>'+
			'<a class="edit" title="" data-toggle="tooltip" data-original-title="Edit" style="display: none;"><i class="fa fa-user-edit"></i></a>'+
			'<a class="delete" title="" data-toggle="tooltip" data-original-title="Delete"><i class="fa fa-trash-alt"></i></a>'+
        	'</form>'+'</tr>';
    	$("table").append(row);		
		// $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
  //       $('[data-toggle="tooltip"]').tooltip();
    });
	// Add row on add button click
	$(document).on("click", ".add", function(){
		var empty = false;
		var input = $(this).parents("tr").find('input[type="text"]');
        input.each(function(){
			if(!$(this).val()){
				$(this).addClass("error");
				empty = true;
			} else{
                $(this).removeClass("error");
            }
		});
		$(this).parents("tr").find(".error").first().focus();
		if(!empty){
			input.each(function(){
				$(this).parent("td").html($(this).val());
			});			
			$(this).parents("tr").find(".add, .edit").toggle();
			$(".add-new").removeAttr("disabled");
		}		
    });
	// Edit row on edit button click
	$(document).on("click", ".edit", function(){		
        $(this).parents("tr").find("td:not(:last-child)").each(function(){
			$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
		});		
		$(this).parents("tr").find(".add, .edit").toggle();
		$(".add-new").attr("disabled", "disabled");
    });
	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
        $(this).parents("tr").remove();
		$(".add-new").removeAttr("disabled");
    });
});
