using UnityEngine;

public class QuadCreator : MonoBehaviour
{
    public Material quadMaterial;  // Optionally set a material in the inspector.

    public void CreateQuad(Vector3 position, float width, float height)
    {
        // Create a new GameObject named "Quad"
        GameObject quad = new GameObject("Quad");

        // Set the quad's position
        quad.transform.position = position;

        // Add MeshFilter and MeshRenderer components
        MeshFilter meshFilter = quad.AddComponent<MeshFilter>();
        MeshRenderer meshRenderer = quad.AddComponent<MeshRenderer>();

        // Define the quad's vertices and triangles
        Mesh mesh = new Mesh
        {
            vertices = new[]
            {
                new Vector3(-width * 0.5f, -height * 0.5f, 0),
                new Vector3(width * 0.5f, -height * 0.5f, 0),
                new Vector3(-width * 0.5f, height * 0.5f, 0),
                new Vector3(width * 0.5f, height * 0.5f, 0)
            },
            triangles = new[] {0, 2, 1, 2, 3, 1},
            normals = new[]
            {
                -Vector3.forward,
                -Vector3.forward,
                -Vector3.forward,
                -Vector3.forward
            },
            uv = new[]
            {
                new Vector2(0, 0),
                new Vector2(1, 0),
                new Vector2(0, 1),
                new Vector2(1, 1)
            }
        };

        // Assign the mesh to the MeshFilter
        meshFilter.mesh = mesh;

        // Assign the material (if specified) to the MeshRenderer
        if (quadMaterial)
        {
            meshRenderer.material = quadMaterial;
        }
    }
}
