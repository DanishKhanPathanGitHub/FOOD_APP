let autocomplete;
 
function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            // Set the default country code, e.g., 'lt' for Lithuania
            componentRestrictions: { 'country': ['in'] },
        }
    );
 
    // Specify the function to be called when a prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}
 
function onPlaceChanged() {
    var place = autocomplete.getPlace();
 
    // Reset the input field or show an alert if the user did not select a prediction
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    } else {
        //console.log('place name =>', place.name);
    }
    // Get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder(); 
    var address = document.getElementById('id_address').value;
 
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            // Update values using jQuery
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);
 
            // Loop through address components and assign other address data
            for (var i = 0; i < place.address_components.length; i++) {
                for (var j = 0; j < place.address_components[i].types.length; j++) {
                    if (place.address_components[i].types[j] == 'country') {
                        $('#id_country').val(place.address_components[i].long_name);
                    }
                    // Get a city
                    if (place.address_components[i].types[j] == 'administrative_area_level_3') {
                        $('#id_city').val(place.address_components[i].long_name);
                    }
                    if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                        $('#id_state').val(place.address_components[i].long_name);
                    }
                    if (place.address_components[i].types[j] == 'postal_code') {
                        $('#id_pincode').val(place.address_components[i].long_name);
                    }else{
                        $('#id_pincode').val('');
                    }
                }
            }
        }
    });
}
 
 
$(document).ready(function(){
    //add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login'
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);  
                    
                    //subtotal, tax, total
                    getCartAmoounts(
                        response.get_cart_total['subtotal'],
                        response.get_cart_total['tax'],
                        response.get_cart_total['total'],
                    )
                }
            }
        })
    })

    //place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
     //decrease to cart
     $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('item-id');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login'
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);    

                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_id);
                        chehckEmptyCart();   
                    }
                    //subtotal, tax, total
                    getCartAmoounts(
                        response.get_cart_total['subtotal'],
                        response.get_cart_total['tax'],
                        response.get_cart_total['total'],
                    )
                }
            }
        })
    })

    $('.delete_cart').on('click', function(e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, "success")
                    removeCartItem(0, cart_id)
                    chehckEmptyCart();

                    //subtotal, tax, total
                    getCartAmoounts(
                        response.get_cart_total['subtotal'],
                        response.get_cart_total['tax'],
                        response.get_cart_total['total'],
                    )
                }
            }
        })
    })  

    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    function chehckEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById("empty-cart").style.display = "block";
        }
    }


    function getCartAmoounts(subtotal, tax, total){
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(total)

        }
    }

});
