let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
		document.getElementById('id_adresa'),
		{
			types: ['geocode', 'establishment'],
            //prikazuj adrese iz hrvatske
			componentRestrictions: {'country': ['hr','de']},
		})

//funkcija koja specificira sto ce se dogoditi kada se pritisne na predikciju(autocomplete)
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged(){
	var place = autocomplete.getPlace();
	
    //korisnik nije pritisnuo na predikciju. Resetiraj polje unosa ili izbaci alert
	if(!place.geometry){
		document.getElementById('id_adresa').placeholder = "Počnite pisati...";
	}
	else{
		//console.log('place name=>', place.name);
	}

    //dohvati komponente adrese i ispuni preostala polja u formi s njima
    //console.log(place);
    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById('id_adresa').value;
    
    
    geocoder.geocode({'address': address}, function(results, status){
        //console.log('results=>', results);
        //console.log('status=>', status);
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            //console.log('lat=>', latitude);
            //console.log('lng=>', longitude);
            $('#id_latituda').val(latitude);
            $('#id_longituda').val(longitude);
            $('#id_adresa').val(address);
        };

    });

    //iteriranje kroz komponente adrese
    console.log(place.address_components)
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            //dohvati drzavu
            if(place.address_components[i].types[j] == 'country'){
                $('#id_drzava').val(place.address_components[i].long_name);
            }
            //dohvati zupaniju
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_zupanija').val(place.address_components[i].long_name);
            }
            //dohvati grad
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_grad').val(place.address_components[i].long_name);
            }
            //dohvati postanski broj
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_postanski_broj').val(place.address_components[i].long_name);
            }else{
                $('#id_postanski_broj').val("");
            }
        }
    }
}	
	


$(document).ready(function(){
    $('.dodaj_proizvod_u_kosaricu').on('click', function(e){
        e.preventDefault();
        
        proizvod_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response);
                if(response.status == 'potrebna_prijava'){
                    Swal.fire({
                        icon: "info",
                        title: "Niste prijavljeni...",
                        text: response.poruka,
                        footer: '<a href="/prijava/">PRIJAVI ME</a>'
                    });
                }else if(response.status == 'Neuspješno'){
                    Swal.fire({
                        icon: "error",
                        title: "Došlo je do pogreške...",
                        text: response.poruka,
                    });
                }             
                else{
                    $('#prikaz_kolicine_proizvoda').html(response.brojac_kosarice['kolicina_proizvoda_u_kosarici']);
                    $('#kolicina-'+proizvod_id).html(response.kolicina);

                    //ukupna_cijena_proizvoda, pdv, ukupan_iznos
                    primjeniIznosKosarice(
                        response.iznos_kosarice['ukupna_cijena_proizvoda'],
                        response.iznos_kosarice['pdv'],
                        response.iznos_kosarice['ukupan_iznos']
                    )
                }              
            }
        })
    })

    $('.kolicina_proizvoda').each(function(){
        var kolicina_id = $(this).attr('id');
        var kolicina = $(this).attr('data-qty');
        $('#'+kolicina_id).html(kolicina);
    })

    $('.izbrisi_proizvod_iz_kosarice').on('click', function(e){
        e.preventDefault();
        
        proizvod_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        id_kosarice = $(this).attr('id');
        
        $.ajax({
            type: 'GET',
            url: url,       
            success: function(response){
                console.log(response);
                if(response.status == 'potrebna_prijava'){
                    Swal.fire({
                        icon: "info",
                        title: "Niste prijavljeni...",
                        text: response.poruka,
                        footer: '<a href="/prijava/">PRIJAVI ME</a>'
                    });
                }else if(response.status == 'Neuspješno'){
                    Swal.fire({
                        icon: "error",
                        title: "Došlo je do pogreške...",
                        text: response.poruka,
                    });
                }else{
                    $('#prikaz_kolicine_proizvoda').html(response.brojac_kosarice['kolicina_proizvoda_u_kosarici']);
                    $('#kolicina-'+proizvod_id).html(response.kolicina);
                    
                    primjeniIznosKosarice(
                        response.iznos_kosarice['ukupna_cijena_proizvoda'],
                        response.iznos_kosarice['pdv'],
                        response.iznos_kosarice['ukupan_iznos']
                    )

                    if(window.location.pathname=='/kosarica/'){
                        ukloniProizvodIzKosarice(response.kolicina, id_kosarice);
                        provjeraKolicineUnutarKosarice();
                    }                 
                }              
            }
        })
    })

    //obrisi proizvod u potpunosti iz kosarice
    $('.obrisi_kosaricu').on('click', function(e){
        e.preventDefault();
        
        id_kosarice = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,       
            success: function(response){
                console.log(response);
                if(response.status == 'Neuspješno'){
                    Swal.fire({
                        icon: "error",
                        title: "Došlo je do pogreške...",
                        text: response.poruka,
                    });
                }else{
                    $('#prikaz_kolicine_proizvoda').html(response.brojac_kosarice['kolicina_proizvoda_u_kosarici']);
                    Swal.fire({
                        title: response.status,
                        text: response.poruka,
                        icon: "success"
                      });
                    
                    primjeniIznosKosarice(
                        response.iznos_kosarice['ukupna_cijena_proizvoda'],
                        response.iznos_kosarice['pdv'],
                        response.iznos_kosarice['ukupan_iznos']
                    )  

                    ukloniProizvodIzKosarice(0, id_kosarice);
                    provjeraKolicineUnutarKosarice();    

                }              
            }
        })
    })

    function ukloniProizvodIzKosarice(kolicina_proizvoda_u_kosarici, id_kosarice){        
            if (kolicina_proizvoda_u_kosarici <= 0){
                document.getElementById('proizvod_u_kosarici-'+id_kosarice).remove();
            }
    }

    function provjeraKolicineUnutarKosarice(){
        var brojacProizvoda = document.getElementById('prikaz_kolicine_proizvoda').innerHTML;
        if (brojacProizvoda == 0){
            document.getElementById('prazna_kosarica').style.display = "block";
        }
    }

    function primjeniIznosKosarice(ukupna_cijena_proizvoda, pdv, ukupan_iznos){
        if(window.location.pathname=='/kosarica/'){
            $('#ukupna_cijena_proizvoda').html(ukupna_cijena_proizvoda);
            $('#pdv').html(pdv);
            $('#ukupan_iznos').html(ukupan_iznos);
        }
    }
});