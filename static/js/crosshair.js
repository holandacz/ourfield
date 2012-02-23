(function() {
  var center_div, center_html, crosshair_div, gv_hidden_crosshair_is_still_hidden, mouse_div;

  if (opts["zoom"] === "auto" || (!opts["zoom"] && opts["zoom"] !== "0")) {
    if (!opts["center"] || (opts["center"] && opts["center"].length === 0)) {
      opts["center"] = [40, -100];
    }
    map.setCenter(new GLatLng(opts["center"][0], opts["center"][1]), 8, eval(opts["map_type"] || "G_NORMAL_MAP"));
  } else {
    map.setCenter(new GLatLng(opts["center"][0], opts["center"][1]), opts["zoom"], eval(opts["map_type"] || "G_NORMAL_MAP"));
  }

  if (opts["center_coordinates"] !== false) {
    if (!$("gv_center_container")) {
      center_div = document.createElement("div");
      center_div.id = "gv_center_container";
      center_div.style.display = "none";
      center_html = "";
      center_html = "<table style=\"cursor:crosshair; filter:alpha(opacity=80); -moz-opacity:0.80; opacity:0.80;\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\"><tr valign=\"middle\"><td><div id=\"gv_center_coordinates\" class=\"gv_center_coordinates\" onclick=\"GV_Toggle('gv_crosshair'); gv_crosshair_temporarily_hidden = false;\" title=\"Click here to turn center crosshair on or off\"></div></td>";
      if (opts["measurement_tools"] !== false) {
        center_html += "<td><div id=\"gv_measurement_icon\" style=\"display:block; width:23px; height:15px; margin-left:3px; cursor:pointer;\"><a href=\"javascript:void(0);\" onclick=\"GV_Place_Measurement_Tools();\" title=\"Click here for measurement tools\" style=\"cursor:pointer;\"><img src=\"http://maps.gpsvisualizer.com/google_maps/ruler.gif\" width=\"23\" height=\"13\" border=\"0\" vspace=\"1\" class=\"gmnoprint\" /></a></div></td>";
      }
      center_html += "</tr></table>";
      center_div.innerHTML = center_html;
      map.getContainer().appendChild(center_div);
    }
    GV_Place_Control(map, "gv_center_container", G_ANCHOR_BOTTOM_LEFT, 4, 40);
    if (!$("gv_crosshair_container")) {
      crosshair_div = document.createElement("div");
      crosshair_div.id = "gv_crosshair_container";
      crosshair_div.style.display = "none";
      crosshair_div.className = "gmnoprint";
      crosshair_div.innerHTML = "<div id=\"gv_crosshair\" align=\"center\" style=\"width:15px; height:15px; display:block;\"><img src=\"http://maps.gpsvisualizer.com/google_maps/crosshair.gif\" alt=\"\" width=\"15\" height=\"15\" style=\"cursor:crosshair;\" /></div>";
      map.getContainer().appendChild(crosshair_div);
    }
    if ($("gv_crosshair")) {
      $("gv_crosshair").style.display = (opts["crosshair_hidden"] ? "none" : "block");
      gv_hidden_crosshair_is_still_hidden = true;
    }
    GV_Setup_Crosshair(map, {
      crosshair_container_id: "gv_crosshair_container",
      crosshair_graphic_id: "gv_crosshair",
      crosshair_width: 15,
      center_coordinates_id: "gv_center_coordinates",
      fullscreen: opts["full_screen"]
    });
  }

  if (opts["mouse_coordinates"]) {
    if (!$("gv_mouse_container")) {
      mouse_div = document.createElement("div");
      mouse_div.id = "gv_mouse_container";
      mouse_div.style.display = "none";
      mouse_div.innerHTML = "<table style=\"cursor:crosshair; filter:alpha(opacity=80); -moz-opacity:0.80; opacity:0.80;\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\"><tr><td><div id=\"gv_mouse_coordinates\" class=\"gv_mouse_coordinates\">Mouse:&nbsp;</div></td></tr></table>";
      map.getContainer().appendChild(mouse_div);
    }
    GV_Place_Control(map, "gv_mouse_container", G_ANCHOR_BOTTOM_LEFT, 4, 58);
    GEvent.addListener(map, "mousemove", function(mouse_coords) {
      if ($("gv_mouse_coordinates")) {
        return $("gv_mouse_coordinates").innerHTML = "Mouse: <span id=\"mouse_coordinate_pair\">" + parseFloat(mouse_coords.lat().toFixed(5)) + "," + parseFloat(mouse_coords.lng().toFixed(5)) + "</span>";
      }
    });
  }

  if (opts["measurement_tools"] && opts["measurement_tools"]["visible"]) {
    GV_Place_Measurement_Tools(opts["measurement_tools"]);
  }

}).call(this);
