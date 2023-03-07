// for new account sidebar with all buttons - collapsible feature
var i;
var j;

var coll = document.getElementsByClassName("collapsible_btn");

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
 
        // de-active the previous active sidebar nested button
        prev_active = document.getElementsByClassName("active_side_group_btn");
        // there can only be 1 or 0 active side group button at a time
        if (prev_active.length) {
            if (prev_active[0] != this) {
                var content = prev_active[0].nextElementSibling;
                content.style.maxHeight = null;    
                prev_active[0].classList.toggle("active_side_group_btn")
            }    
        }

        // active the current sidebar nested button
        this.classList.toggle("active_side_group_btn");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        } 
        
    });
}


// clicking sidebar nested button
var nested_btns = document.getElementsByClassName("nested_btn");

for (i = 0; i < nested_btns.length; i++) {
    nested_btns[i].addEventListener("click", function() {

        // de-active the previous active sidebar nested buttons
        prev_active = document.getElementsByClassName("active_nested_btn");
        for (j = 0; j < prev_active.length; j++) {
            prev_active[j].classList.toggle("active_nested_btn")
        }
        this.classList.toggle("active_nested_btn");

        // getting the id of the table to view
        var page_name = document.getElementsByClassName("active_nested_btn")[0].name

        // de-active previous active tables
        prev_table = document.getElementsByClassName("active_table");
        if (prev_table.length) {
            prev_table[0].classList.toggle("active_table");
        }


        // tip: getElementById returns only one element
        current_table = document.getElementById(page_name);
        current_table.classList.toggle("active_table");

        // changing page topic in blue bar
        current_page_name = document.getElementsByClassName("pagetopic");
        var page_topic = document.getElementsByClassName("active_nested_btn")[0].innerText
        current_page_name[0].innerText = page_topic

        


        
    });
}










// ---------------------------------------------------------------------------------
// When in transaction history page

var page_btns = document.getElementsByClassName("page_button");
// getting all page btns then toggle active, then toggle the selected page btn

// making the first page button toggle
if (page_btns.length > 1) {
    page_btns[0].classList.toggle("active_page_btn");    
}

// making the first transaction page toggle
var all_tr_lists = document.getElementsByClassName("tr_list");
if (all_tr_lists.length > 1) {
    all_tr_lists[0].classList.toggle("active_tr_list");    
}

for (i = 0; i < page_btns.length; i++) {
    page_btns[i].addEventListener("click", function() {
    
        // de-active the page button
        var all_active_page_btns = document.getElementsByClassName("active_page_btn");
        for (j = 0; j < all_active_page_btns.length; j++) {
            all_active_page_btns[j].classList.toggle("active_page_btn")
        }

        // de-active the transaction page
        var all_active_tr_pages = document.getElementsByClassName("active_tr_list");
        for (j = 0; j < all_active_tr_pages.length; j++) {
            all_active_tr_pages[j].classList.toggle("active_tr_list")
        }

        // active the page button
        this.classList.toggle("active_page_btn")  
        
        // active the transaction page
        var all_active_page_btns = document.getElementsByClassName("active_page_btn");
        var num = all_active_page_btns[0].id.slice(4)

        var all_tr_lists = document.getElementsByClassName("tr_list");
        all_tr_lists[num-1].classList.toggle("active_tr_list");
    });
}


// ---------------------------------------------------------------------------------

// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  
// OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  OLD  

// ---------------------------------------------------------------------------------
// for account sidebar - collapsible feature
var coll = document.getElementsByClassName("collapsible");
var i;
var j;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active_side_btn");
        var content = this.nextElementSibling;
        if (content.style.maxHeight){
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        } 
        
    });
}

// ---------------------------------------------------------------------------------

var maintab = document.getElementsByClassName("main_opt");

for (i = 0; i < maintab.length; i++) {
    maintab[i].addEventListener("click", function() {
        this.classList.toggle("active_opt");        
    });
    
}
