$(document).ready(function() {
    // console.log($("a:contains('Table of Contents')").parent().siblings());
    let search_form = "<li data-action='search'><form class=\"search\" action=\"search.html\" method=\"get\">\n" +
                      "      <input type=\"text\" name=\"q\" aria-labelledby=\"searchlabel\" placeholder=\"\">\n" +
                      "      <input type=\"submit\" value=\"Search\">\n" +
                      "</form></li>"

    let dyn_context_menu = "<ul class='custom-menu'>" + search_form
    $("a:contains('Table of Contents')").parent().siblings("ul").children().each(function(){
        let a = $(this).find("a");
        let a_class = a.attr("class");
        let a_href = a.attr("href");
        let a_text = a.text();
        console.log(a_text + " - " + a_class + " - " + a_href);

        if (a_href != "#") {
            dyn_context_menu = dyn_context_menu + "<li data-action='" + a_href + "'>" + a_text + "</li>";
        }
    });
    dyn_context_menu = dyn_context_menu + "<li style='text-align:center;'>•••••••</li>";
    dyn_context_menu = dyn_context_menu + "<li data-action='index.html'>Package corelibs</li>";
    dyn_context_menu = dyn_context_menu + "<li data-action='genindex.html'>Index</li>";
    dyn_context_menu = dyn_context_menu + "<li data-action='py-modindex.html'>Module Index</li>";
    dyn_context_menu = dyn_context_menu + "<li data-action='search.html'>Search Page</li>";
    $('body').append(dyn_context_menu + "</ul>");

    $(".custom-menu li").click(function(){
        if ($(this).attr("data-action") && $(this).attr("data-action") !== "search") {
            window.location = $(this).attr("data-action");
            $(".custom-menu").hide(100);
        }
    });
}).bind("contextmenu", function (event) {
    event.preventDefault();
    $(".custom-menu").finish().toggle(100).css({
        top: event.pageY + "px",
        left: event.pageX + "px"
    });
}).bind("mousedown", function (e) {
    if (!$(e.target).parents(".custom-menu").length > 0) {
        $(".custom-menu").hide(100);
    }
});