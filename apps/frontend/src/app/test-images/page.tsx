export default function TestImagesPage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Test Images</h1>

      <div className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold mb-2">Direct IGDB Image URL:</h2>
          <img
            src="https://images.igdb.com/igdb/image/upload/t_thumb/co1uii.jpg"
            alt="Test IGDB Image"
            className="max-w-xs border"
          />
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-2">Generic Test Image:</h2>
          <img
            src="https://httpbin.org/image/jpeg"
            alt="Test Generic Image"
            className="max-w-xs border"
          />
        </div>
      </div>
    </main>
  );
}
