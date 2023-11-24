class Api::V1::ProjectsController < ApplicationController
  def index
    projects = Project.all
    render json:projects, status:200
  end

  def show
    projects = Project.find(params[:id])
    if projects
      render json:projects, status:200
    else
      render json: {error: "Error finding project"}, status:404
    end
  end

  def create
    projects = Project.new(project_params)

    if projects.save
      render json:projects, status:200
    else
      render json: {error: "Error creating project"}, status:400
    end
  end

  def update
    projects = Project.find(params[:id])

    if projects.update(project_params)
      render json:projects, status:200
    else
      render json: {error: "Error updating project"}, status:400
    end
  end

  private
    def project_params
      params.require(:project).permit(:name, :description, :project_type_id, :completed)
    end
end
