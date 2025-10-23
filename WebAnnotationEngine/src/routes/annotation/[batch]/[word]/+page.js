export async function load({ params, fetch }) {
  const { batch, word } = params;

  const response = await fetch('http://localhost:5000/api/batches');

  if (!response.ok) {
    console.error('Failed to fetch batches');
    throw new Error('Failed to load batch data');
  }

  const batches = await response.json();

  const selectedBatch = batches[batch];
  if (!selectedBatch) {
    throw new Error(`Batch "${batch}" not found`);
  }

  const selectedVideoData = selectedBatch[word];
  if (!selectedVideoData) {
    throw new Error(`Word "${word}" not found in batch "${batch}"`);
  }

  return {
    batch,
    word,
    selectedVideoData,
  };
}
