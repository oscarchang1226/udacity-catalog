$(".menu-button").on("click", function() {
    $("header div.options").toggleClass("show-menu");
});

$(".filter-button").on("click", function() {
    $("nav").toggleClass("show-filter");
});
