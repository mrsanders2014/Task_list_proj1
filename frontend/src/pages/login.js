import React from 'react';
import { useRouter } from 'next/router';

const LoginRedirect = () => {
  const router = useRouter();
  
  React.useEffect(() => {
    router.replace('/');
  }, [router]);
  
  return null;
};

export default LoginRedirect;
