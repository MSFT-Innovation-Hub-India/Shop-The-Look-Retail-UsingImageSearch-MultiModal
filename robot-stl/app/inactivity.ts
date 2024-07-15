let timeout: NodeJS.Timeout;

function resetTimer() {
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    window.location.href = '/'; // Redirect to homepage
  }, 0.5 * 60 * 1000); // 5 minutes inactivity timeout
}

export function startInactivityDetection() {
  const events: string[] = ['mousemove', 'keydown', 'scroll', 'click'];

  events.forEach(event => {
    window.addEventListener(event, resetTimer);
  });

  resetTimer(); // Initialize timer
}
