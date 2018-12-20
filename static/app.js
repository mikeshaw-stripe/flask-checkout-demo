var stripe = Stripe('pk_test_vM25HSU3TtQMcDTtAYQU1CuA', {
  betas: ['checkout_beta_4']
});

function handleClick(button) {
  // Generic eventListener for calling Stripe checkout
  stripe.redirectToCheckout({
    items: [{plan: button.dataset.plan, quantity: 1}],

    // Note that it is not guaranteed your customers will be redirected to this
    // URL *100%* of the time, it's possible that they could e.g. close the
    // tab between form submission and the redirect.
    successUrl: `https://${window.location.hostname}/success`,
    cancelUrl: `https://${window.location.hostname}`,
    })
    .then(function (result) {
      if (result.error) {
        // If `redirectToCheckout` fails due to a browser or network
        // error, display the localized error message to your customer.
      var displayError = document.getElementById('error-message');
        displayError.textContent = result.error.message;
      }
    });
};