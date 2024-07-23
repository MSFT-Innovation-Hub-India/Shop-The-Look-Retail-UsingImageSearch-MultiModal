import type { NextApiRequest, NextApiResponse } from 'next';

type Data = {
  message: string;
  imageURL?: string;
};

export default function handler(req: NextApiRequest, res: NextApiResponse<Data>) {
  const { message, imageURL } = req.body;
  res.status(200).json({ message, imageURL });
}