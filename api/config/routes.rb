Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :videos
      resources :sections
      resources :courses
      resources :course_types
    end
  end
end
