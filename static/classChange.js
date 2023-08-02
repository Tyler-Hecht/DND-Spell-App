function classChange(select) {
    var selected = select.options[select.selectedIndex].value;
    $.get("/class/" + selected, function(data) {
        // Update the table content without changing the URL
        $("#table-content").html(data);
        // make sidebar visible
        if (selected != "Select Class") {
            $("#sidebar-text").removeAttr("hidden");
        } else {
            $("#sidebar-text").attr("hidden", true);
        }
        // change title
        if (selected != "Select Class") {
            $("#title").html(selected + " Spells");
        } else {
            $("#title").html("DND Spells");
        }

        var paladin_color = "#efc17c"
        var sorcerer_color = "#b1d9f5"
        var bard_color = "#d9b1f5"
        var wizard_color = "#c44f74"

        // hide sidebar when class is changed
        $("#close-sidebar").attr("hidden", true);
        $("#sidebar-text").attr("hidden", true);
        $("#spell-title").attr("hidden", true);
        $("#sidebar").attr("hidden", true);

        if (selected == "Select Class") {
            $("#sidebar").attr("hidden", true);
            $("#table-content").attr("hidden", true);
            $("#default-text").removeAttr("hidden");
            $("#filters").attr("hidden", true);
            $("body").css("background-color", "#f9f7ed");
        } else {
            $("#sidebar").removeAttr("hidden");
            $("#sidebar-text").attr("hidden", true);
            $("#sidebar-default-text").removeAttr("hidden");
            $("#table-content").removeAttr("hidden");
            $("#default-text").attr("hidden", true);
            $("#filters").removeAttr("hidden");
            document.getElementsByClassName("scrollit")[0].id = selected.toLowerCase();
            document.getElementsByClassName("scrollit")[1].id = selected.toLowerCase();
            if (selected == "Paladin") {
                $("#fullCaster").attr("hidden", true);
                $("body").css("background-color", paladin_color);
            } else if (selected == "Sorcerer") {  
                $("#fullCaster").removeAttr("hidden");
                $("body").css("background-color", sorcerer_color);
            } else if (selected == "Bard") {
                $("#fullCaster").removeAttr("hidden");
                $("body").css("background-color", bard_color);
            } else if (selected == "Wizard") {
                $("#fullCaster").removeAttr("hidden");
                $("body").css("background-color", wizard_color);
            }
            
            // add "example" option to #subclass-select select element
            select = document.getElementById("subclass-select");
            var option = document.createElement("option");
            option.text = "Example";
            option.value = "Example";
            select.add(option);
        }
    });
}
