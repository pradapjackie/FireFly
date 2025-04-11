import React, { Suspense } from 'react';
import { Loading } from 'components/Loading/Loading';

export const CustomSuspense = ({ children }) => (
  <Suspense fallback={<Loading />}>{children}</Suspense>
);
