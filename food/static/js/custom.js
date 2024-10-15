let autocompleteAddress, autocompleteLocation;
 
function initAutoComplete() {
    // Initialize autocomplete for the address field
    autocompleteAddress = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { 'country': ['in'] }, // Limit to a specific country
        }
    );

    // Add listener for address input
    autocompleteAddress.addListener('place_changed', onPlaceChangedAddress);

    // Initialize autocomplete for the location field
    autocompleteLocation = new google.maps.places.Autocomplete(
        document.getElementById('id_location'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { 'country': ['in'] },
        }
    );

    // Add listener for location input
    autocompleteLocation.addListener('place_changed', onPlaceChangedLocation);
}

function onPlaceChangedLocation() {
    var place = autocompleteLocation.getPlace();
 
    // Reset the input field or show an alert if the user did not select a prediction
    if (!place.geometry) {
        document.getElementById('id_location').placeholder = "Start typing...";
    } else {
        //console.log('place name =>', place.name);
    }
    // Get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder();
    var location = document.getElementById('id_location').value;
    
    geocoder.geocode({ 'location': location }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            $('#id_latitude1').val(latitude);

            $('#id_longitude1').val(longitude);
            
            $('#id_location').val(longitude);
        }
    });
}



function onPlaceChangedAddress() {
    var place = autocompleteAddress.getPlace();
 
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


document.addEventListener('DOMContentLoaded', function () {
    // Toggle the dropdown menu when the trigger is clicked
    const dropdownTrigger = document.querySelector('.dropdown > a');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    dropdownTrigger.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default link behavior
        event.stopPropagation(); // Prevent event bubbling
        dropdownMenu.style.display = (dropdownMenu.style.display === 'block') ? 'none' : 'block';
    });

    // Close the dropdown menu when clicking outside of it
    document.addEventListener('click', function (event) {
        if (!event.target.closest('.dropdown')) {
            dropdownMenu.style.display = 'none';
        }
    });
});
 
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
                        response.get_cart_total['taxtotal'],
                        response.get_cart_total['total'],
                        response.get_cart_total['taxes'],
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
                        response.get_cart_total['taxtotal'],
                        response.get_cart_total['total'],
                        response.get_cart_total['taxes'],
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
                    window.location.href = '/cart/';
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


    function getCartAmoounts(subtotal, taxtotal, total, taxes) {
        if (window.location.pathname == '/cart/') {
            // Update subtotal and total
            $('.subtotal').html(subtotal);
            $('#total').html(total);
            $('#taxtotal').html(taxtotal);
    
            // Update each tax type individually
            $.each(taxes, function(taxtype, taxes) {
                var taxPercentage = taxes[0]; // This is the tax percentage
                var taxAmount = taxes[1];     // This is the tax amount
    
                // Update the tax amount in the DOM based on the tax type
                $('#tax-' + taxtype).html(taxAmount);
            });
        }
    }

    $('.add_hour').on('click', function(e) {
        e.preventDefault();
        var day = document.getElementById('id_day').value;
        var from_hour = document.getElementById('id_from_hour').value;
        var to_hour = document.getElementById('id_to_hour').value;
        var is_closed = document.getElementById('id_is_closed').checked;
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        var url = document.getElementById('add_hour_url').value;
    
        // Condition to validate the form input
        var condition = "(is_closed && from_hour == '' && to_hour == '') || (!is_closed && from_hour != '' && to_hour != '')";
        if (day != '') {
            if (eval(condition)) {
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        'day': day,
                        'from_hour': from_hour,
                        'to_hour': to_hour,
                        'is_closed': is_closed,
                        'csrfmiddlewaretoken': csrf_token,
                    },
                    success: function(response) {
                        if (response.status == 'success') {
                            var existingRow = $(`#hour-${response.id}`);
                            var html;
    
                            if (response.is_closed == 'Closed') {
                                html = `Closed`;
                            } else {
                                html = `${response.from_hour} - ${response.to_hour}`;
                            }
    
                            // Update the existing row
                            existingRow.find('td:nth-child(2)').html(html);
    
                            document.getElementById('opening_hours').reset();
                            swal(response.message, '', 'success');
                        } else {
                            swal(response.message, '', 'error');
                            console.log(response.message)
                        }
                    }
                });
            } else {
                swal('Select hours or closed. You cannot select both. Fill both "from" and "to" hour fields if you are filling hours.', '', 'error');
            }
        } else {
            swal("Please fill the required fields", '', 'error');
        }
    });
    

});
