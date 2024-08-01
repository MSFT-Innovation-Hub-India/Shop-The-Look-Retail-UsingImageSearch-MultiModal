// hooks/useThread.ts
'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const useThread = () => {
  const [threadId, setThreadId] = useState<string | null>(null);

  useEffect(() => {
    const storedThreadId = sessionStorage.getItem('threadId');
    if (storedThreadId) {
      setThreadId(storedThreadId);
      console.log('Stored Thread ID:', storedThreadId);
    } else {
      axios.post(process.env.NEXT_PUBLIC_CREATE_THREAD_ENDPOINT || '')
        .then(response => {
          if (response.status === 200) {
            const thread_id = response.data.thread_id;
            console.log('Thread ID:', thread_id);
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
