import { NextRequest, NextResponse } from "next/server"

async function handler(
  request: NextRequest,
  { params }: { params: Promise<{ segments: string[] }> }
) {
  try {
    // Build target URL
    const { segments } = await params;
    const baseUrl = process.env.NEXT_PUBLIC_MUNA_API_URL ?? "https://api.muna.ai/v1";
    const path = segments?.join("/") ?? "";
    const targetUrl = new URL(path, `${baseUrl}/`);
    targetUrl.search = request.nextUrl.search;
    // Build headers
    const headers = new Headers(request.headers);
    headers.set("Authorization", `Bearer ${process.env.MUNA_ACCESS_KEY}`);
    headers.set("x-forwarded-host", request.headers.get("host") ?? "");
    headers.set(
      "x-forwarded-proto",
      request.headers.get("x-forwarded-proto") ?? request.nextUrl.protocol.replace(":", ""),
    );
    headers.delete("host");           // recompute
    headers.delete("content-length"); // recompute
    // Build request
    const hasBody = !["GET", "HEAD"].includes(request.method.toUpperCase());
    const init: RequestInit & { duplex?: "half" } = {
      method: request.method,
      headers,
      redirect: "manual",
    }
    if (hasBody && request.body) {
      init.body = request.body;
      init.duplex = "half";
    }
    // Request
    const response = await fetch(targetUrl.toString(), init);
    // Respond
    const responseHeaders = new Headers(response.headers);
    responseHeaders.delete("content-length");
    responseHeaders.delete("content-encoding");
    responseHeaders.delete("transfer-encoding");
    responseHeaders.delete("x-middleware-rewrite");
    return new NextResponse(response.body, {
      status: response.status,
      headers: responseHeaders,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    return Response.json({ errors: [{ message }] }, { status: 500 });
  }
}

export {
  handler as DELETE,
  handler as GET,
  handler as HEAD,
  handler as OPTIONS,
  handler as PATCH,
  handler as POST,
  handler as PUT
};