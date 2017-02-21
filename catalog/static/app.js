$(".menu-button").on("click", function() {
    $("nav").removeClass("show-filter");
    $("header div.options").toggleClass("show-menu");
});

$(".filter-button").on("click", function() {
    $("header div.options").removeClass("show-menu");
    $("nav").toggleClass("show-filter");
});

$("main").on("click", function() {
    $("header div.options").removeClass("show-menu");
    $("nav").removeClass("show-filter");
});
