// checked == 0: unchecked, checked == 1: fully checked, checked == 2: partially checked
var Tree = [
    {
        "name": "File1",
        "collapsed": false,
        "selected": 0,
        "members": [
            {
                "name": "thisclass",
                "collapsed": false,
                "selected": 0,
                "members": [
                    {"name": "thismethod", "selected": 0},
                    {"name": "thatmethod", "selected": 0},
                    {"name": "method2", "selected": 0},
                ]
            },
            {
                "name": "class2",
                "collapsed": true,
                "selected": 0,
                "members": [
                    {"name": "method1", "selected": 0},
                    {"name": "method2", "selected": 0},
                ]
            },
        ]
    },
    {
        "name": "File2",
        "collapsed": false,
        "selected": 0,
        "members": [
            {
                "name": "class1",
                "collapsed": false,
                "selected": 0,
                "members": [
                    {"name": "method1", "selected": 0},
                    {"name": "method2", "selected": 0},
                ]
            },
            {
                "name": "class2",
                "collapsed": true,
                "selected": 0,
                "members": [
                    {"name": "method1", "selected": 0},
                    {"name": "method2", "selected": 0},
                ]
            },
        ]
    }
];

var TreeObj = {

    idcount: 0,
 
    add: function(parent, list) {
        list.forEach(function (value) {
            // console.log(value.name);
            var item = $("<li>");
            var id = "_" + TreeObj.idcount;
            item.attr("id", "item" + id)
            TreeObj.idcount += 1;
            if ("collapsed" in value) {
                $(item).html("<a href='#', onclick='TreeObj.toggle(\"" + id + "\"); return;' id='span" + id + "'>"  + (value.collapsed ? "&#5125;" : "&#9660;") + " </a>" +
                             "<input id='cb" + id + "' type='checkbox' onclick=TreeObj.select(\"" + id + "\");>" + 
                             "<a href='#', onclick='TreeObj.toggle(\"" + id + "\"); return;'>" + value.name + "</a>")
            } else {
                $(item).html("<input id='cb" + id + "' type='checkbox' onclick=TreeObj.select(\"" + id + "\");>" +
                             "<a href='#' onclick='return;'>" + value.name + "</a>")
            }
            value._id = id;
            $(item).data("value", value);
            $(item).appendTo(parent);            
            if ("members" in value) {
                var elem = $("<ul>");
                $(elem).attr("id", "ul" + id);
                $(elem).css("display", value.collapsed ? "none": "block");
                TreeObj.add(elem, value.members);
                $(elem).appendTo(item)
            }
        });
    },

    toggle: function(whatid) {
        console.log(whatid);
        var data = $("#item" + whatid).data("value");
        data["collapsed"] = !data["collapsed"];
        $("#item" + whatid).data("value", data);
        var elem = $("#ul" + whatid);
        elem.css("display", data["collapsed"] ? "none" : "block");
        $("#span" + whatid).html(data["collapsed"] ? "&#5125;" : "&#9660;");
    },

    select: function(whatid) {
        console.log(whatid);
        checked = $("#cb" + whatid).is(":checked");
        //console.log(checked);
        var data = $("#item" + whatid).data("value");
        data["selected"] = checked ? 1 : 0;
        $("#item" + whatid).data("value", data);

        TreeObj.checkChilds(data, checked);

        Tree.forEach(function (value) {     // iterate files
            var f_state = [];
            value.members.forEach(function (value) {    // iterate classes
                var c_state = [];
                value.members.forEach(function (value) {
                    // check bottom level
                    c_state.push(value.selected);
                });
                if (0) { 
                    console.log("0:" + value.name + c_state);
                    console.log("1:" + c_state.some(e => e == true));
                    console.log("2:" + c_state.every(e => e == false));
                }
                // check mid level 
                if (c_state.every(e => e == 1)) {
                    value.selected = 1;
                    $("#cb" + value._id).prop("checked", true);
                    $("#cb" + value._id).prop("indeterminate", false);
                } else if (c_state.some(e => e == 1)) {
                    value.selected = 2;
                    $("#cb" + value._id).prop("indeterminate", true);
                } else if (c_state.every(e => e == 0)) {
                    value.selected = 0;
                    $("#cb" + value._id).prop("checked", false);
                    $("#cb" + value._id).prop("indeterminate", false);
                }
                f_state.push(value.selected);
            });
            // check top level             
            if (f_state.every(e => e == 1)) {
                value.selected = 1;
                $("#cb" + value._id).prop("checked", true);
                $("#cb" + value._id).prop("indeterminate", false);
                $("#btnpost").prop("disabled", false);
            } else if (f_state.some(e => e >= 1)) {
                value.selected = 2;
                $("#cb" + value._id).prop("indeterminate", true);
                $("#btnpost").prop("disabled", false);
            } else if (f_state.every(e => e == 0)) {
                value.selected = 0;
                $("#cb" + value._id).prop("checked", false);
                $("#cb" + value._id).prop("indeterminate", false);
                $("#btnpost").prop("disabled", true);
            }
            
        });
    },

    checkChilds: function(data, checked) {
        // check/uncheck all childs
        if ("members" in data) {
            data.members.forEach(function (value) {
                value.selected = checked ? 1 : 0;
                $("#cb" + value._id).prop("checked", checked);
                console.log(value.name + value._id);
                TreeObj.checkChilds(value, checked);
            });
        }
    },

    post: function() {
        console.log(JSON.stringify(Tree));
        $("#message").prop("value", JSON.stringify(Tree));
        $("form").submit();
    },

    init: function() {    
        $("#btnpost").prop("disabled", true);
        TreeObj.add($("#tree"), Tree);

/*        
        var data = $(".item2").data();
        alert(data["value"]["selected"] + " " + Tree[0]["members"][0]["members"][0]["selected"]);
        data["value"]["selected"] = true;
        alert(data["value"]["selected"] + " " + Tree[0]["members"][0]["members"][0]["selected"]);
*/        
        //$(".item2").data("selected", {"selected": true});
        //data = $(".item2").data();
        //console.log(data);
        //console.log(Tree[0]["members"][0]["members"][0]);
        //Tree.forEach(TreeObj.add);
    },
 };

var _TreeObj = {
    myProperty: "hello",

    append: function() {
        this.elements = [];
      },

 
    add: function(value) {
        console.log(value.name);
        console.log(this);
        if ("members" in value) {
            value.members.forEach(TreeObj.add);
        }
    },

    init: function() {
        TreeObj.append.prototype.add = function(array) {
            array.forEach(function(entry) {
                console.log(entry);
                this.elements.append(entry);
            }, this);
        };
    
        Tree.forEach(TreeObj.add);
    },
 };
 

$( document ).ready(TreeObj.init);

