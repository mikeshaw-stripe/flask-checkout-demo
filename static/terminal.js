const terminal = StripeTerminal.create({
  // fetchConnectionToken must be a function that returns a promise
  onFetchConnectionToken: fetchConnectionToken,
});

console.log('Do something');
initializeReader();

async function initializeReader() {
  const discoverResult = await terminal.discoverReaders();
  if (discoverResult.error) {
    console.log('Failed to discover: ', discoverResult.error);
  } else if (discoverResult.discoveredReaders.length === 0) {
    console.log('No available readers.');
  } else {
    // You should show the list of discoveredReaders to the
    // cashier here and let them select which to connect to (see below).
    connectReader(discoverResult);
  }
}

async function fetchConnectionToken() {
  // Your backend should call /v1/terminal/connection_tokens and return the JSON response from Stripe
  console.log('Getting connection')
  const response = await fetch(`https://${window.location.hostname + (window.location.port? ":" + window.location.port : "")}/terminal_connection_token`, { method: "POST" });
  const json = await response.json();
  return json.secret;
}

async function connectReader(discoverResult) {
  // Just select the first reader here.
  const selectedReader = discoverResult.discoveredReaders[0];

  const connectResult = await terminal.connectReader(selectedReader);
  if (connectResult.error) {
    console.log('Failed to connect:', connectResult.error);
  } else {
    console.log('Connected to reader:', connectResult.connection.reader.label);
    process();
  }
}

async function process() {
  // clientSecret is the client_secret from the PaymentIntent you created in Step 1.
  const result = await terminal.collectPaymentMethod(clientSecret);
  if (result.error) {
    console.error(`Collect payment method failed: ${result.error.message}`);
  } else {
    console.log("Payment method: ", result.paymentIntent.payment_method);
    // Confirm PaymentIntent (see below)
    confirmPaymentIntent(result.paymentIntent);
  }
}

async function confirmPaymentIntent(paymentIntent) {
  const confirmResult = await terminal.confirmPaymentIntent(paymentIntent);
  if (confirmResult.error) {
    console.error(`Confirm failed: ${confirmResult.error.message}`);
  } else if (confirmResult.paymentIntent) {
    // Placeholder for notifying your backend to capture the PaymentIntent
    const URL = '/capture/' + confirmResult.paymentIntent.id;
    fetch(URL)
    .then(resp => {
        if (!resp.ok) {
            throw resp;
        }
        window.location.href = `https://${window.location.hostname + (window.location.port? ":" + window.location.port : "")}/success`;
    })
    }
  }