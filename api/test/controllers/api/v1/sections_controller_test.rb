require "test_helper"

class Api::V1::SectionsControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get api_v1_sections_index_url
    assert_response :success
  end
end
