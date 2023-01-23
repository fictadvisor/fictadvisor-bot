import { AxiosInstance } from 'axios';

type UpdateCoursePayload = {
    description?: string;
    state?: 'pending' | 'approved' | 'declined';
};

export default (client: AxiosInstance) => {
  const update = (id: string, payload: UpdateCoursePayload) => client.put(`/courses/${id}`, payload);
  const deleteCourse = (id: string) => client.delete(`/courses/${id}`);

  return {
    update,
    delete: deleteCourse,
  };
};
