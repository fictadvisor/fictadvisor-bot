import { AxiosInstance } from 'axios';

type UpdateReviewPayload = {
    state?: 'pending' | 'approved' | 'declined' | 'outdated';
    content?: string;
    rating?: number;
};

export default (client: AxiosInstance) => {
  const update = (id: string, payload: UpdateReviewPayload) => client.put(`/reviews/${id}`, payload);
  const deleteReview = (id: string) => client.delete(`/reviews/${id}`);

  return {
    update,
    delete: deleteReview,
  };
};
