class Api::V1::ProjectTypesController < ApplicationController
  def index
    project_types = ProjectType.all
    render json:project_types, status:200
  end

  def show
    project_types = ProjectType.find(params[:id])
    if project_types
      render json:project_types, status:200
    else
      render json: {error: "Error finding project type"}, status:404
    end
  end

  def create
    project_types = ProjectType.new(project_type_params)

    if project_types.save
      render json:project_types, status:200
    else
      render json: {error: "Error creating project type"}, status:400
    end
  end

  def update
    project_types = ProjectType.find(params[:id])

    if project_types.update(project_type_params)
      render json:project_types, status:200
    else
      render json: {error: "Error creating project type"}, status:400
    end
  end

  private
    def project_type_params
      params.require(:project_type).permit(:name, :color)
    end
end
