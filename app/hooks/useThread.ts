// hooks/useThread.ts
import { useState, useEffect } from 'react';
import axios from 'axios';

const useThread = () => {
  const [threadId, setThreadId] = useState<string | null>(null);

  useEffect(() => {
    const storedThreadId = sessionStorage.getItem('threadId');
    if (storedThreadId) {
      setThreadId(storedThreadId);
    } else {
      axios.post('http://localhost:5328/create-thread')
        .then(response => {
          if (response.status === 200) {
            const thread_id = response.data.thread_id;
            if (thread_id) {
              setThreadId(thread_id);
              sessionStorage.setItem('threadId', thread_id);
            }
          }
        })
        .catch(error => {
          console.error("There was an error creating the thread!", error);
        });
    }
  }, []);

  return threadId;
};

export default useThread;
