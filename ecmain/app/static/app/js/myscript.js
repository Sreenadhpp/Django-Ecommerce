$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  console.log(id);

  var eml = this.parentNode.children[2];
  console.log(eml);

  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success : function(data){
        console.log(data)

        eml.innerText = data.quantity
        document.getElementById("amount").innerText = data.amount
        document.getElementById("totalamount").innerText = data.totalamount
    }
  });

});

$('.minus-cart').click(function(){

    var id = $(this).attr("pid").toString()
    console.log(id)

    var eml = this.parentNode.children[2]
    console.log(eml)

    $.ajax({
        type : "GET",
        url : "/minuscart",
        data : {
            prod_id : id
        },
        success : function(data){
            console.log(data)
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount

            if (data.quantity ==0){
                console.log(data.quantity)
                return eml.parentNode.parentNode.parentNode.parentNode.remove()
            }
        }
    })

})

$('.remove-cart').click(function(){

    var id = $(this).attr("pid").toString()
    console.log(id)

    var eml = this
    console.log(eml)

    $.ajax({
        type : "GET",
        url : "/removecart",
        data : {
            prod_id : id
        },
        success : function(data){
            console.log(data)
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            document.getElementById("totalitem").innerText = data.totalitem
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })

})

$('.plus-wishlist').click(function(){
    var id = $(this).attr('pid').toString();
    console.log(id)

    $.ajax({
        type : "GET",
        url  : '/pluswishlist',
        data : {
            prod_id : id
        },
        success : function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

$('.minus-wishlist').click(function(){
    var id = $(this).attr('pid').toString();

    $.ajax({
        type : "GET",
        url  : '/minuswishlist',
        data : {
            prod_id : id
        },
        success : function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})