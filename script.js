document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upiForm');
    const resultContainer = document.getElementById('result');
    const qrCodeImg = document.getElementById('qrCode');
    const upiLinkElement = document.getElementById('upiLink');
    const downloadBtn = document.getElementById('downloadBtn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const upiId = document.getElementById('upiId').value.trim();
        const name = document.getElementById('name').value.trim();
        const amount = document.getElementById('amount').value.trim();

        try {
            const response = await fetch('/generate-qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    upiId,
                    name,
                    amount
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate QR code');
            }

            // Display results
            qrCodeImg.src = data.qrCode;
            upiLinkElement.textContent = data.upiLink;
            resultContainer.classList.remove('hidden');

            // Setup download button
            downloadBtn.onclick = () => {
                const link = document.createElement('a');
                link.download = 'upi_payment_qr.png';
                link.href = data.qrCode;
                link.click();
            };
        } catch (error) {
            alert(error.message || 'Error generating QR code. Please try again.');
            console.error('QR Code generation error:', error);
        }
    });
});