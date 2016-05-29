---
title: DX11 APP Framework
date: 2016-05-29 21:39:56
tags: GPU
categories: CG
---

学习用，不断更新中。

```c
WinMain

    SystemClass* System->Initialize()

        SystemClass::InitializeWindwos()  // fullScreen?  init and run windows

        InputClass* m_Input->Initialize()  // m_keys[0~255] = false

        GraphicsClass* m_Graphics->Initialize()

            D3DClass* m_Direct3D->Initializae()

                bool InitRefreshRate(bool, int, int);

            bool GraphicsClass::CreateSwapChainAndDev(int, int, bool, HWND);

                D3D11CreateDeviceAndSwapChain()

            bool GraphicsClass::CreateBackBuffer();

                IDXGISwapChain* m_swapChain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&backBufferPtr)
                ID3D11Device* m_device->CreateRenderTargetView(backBufferPtr, NULL, &m_renderTargetView);


            bool GraphicsClass::CreateDepthBuffer(int, int);

                ID3D11Device* m_device->CreateTexture2D(&depthBufferDesc, NULL, &m_depthStencilBuffer);

            bool GraphicsClass::CreateDepthStenci();

                ID3D11Device* m_device->CreateDepthStencilState(&depthStencilDesc, &m_depthStencilState);
                ID3D11DeviceContext* m_deviceContext->OMSetDepthStencilState(m_depthStencilState, 1);
                ID3D11Device* m_device->CreateDepthStencilView(m_depthStencilBuffer, &depthStencilViewDesc, &m_depthStencilView);
                ID3D11DeviceContext* m_deviceContext->OMSetRenderTargets(1, &m_renderTargetView, m_depthStencilView);


            bool GraphicsClass::CreateRasterizer();

                D3D11_RASTERIZER_DESC rasterDesc.FillMode = D3D11_FILL_SOLID or D3D11_FILL_WIREFRAME
                ID3D11Device* m_device->CreateRasterizerState(&rasterDesc, &m_rasterState);
                ID3D11DeviceContext* m_deviceContext->RSSetState(m_rasterState);

            bool GraphicsClass::CreateRenderMatrix(int, int, float, float);

                D3D11_VIEWPORT viewport;
                float fieldOfView = 3.141592654f / 4.0f;
                float screenAspect = (float)screenWidth / (float)screenHeight;
                m_projectionMatrix = XMMatrixPerspectiveFovLH(fieldOfView, screenAspect, screenNear, screenDepth);
                m_worldMatrix = XMMatrixIdentity();
                m_orthoMatrix = XMMatrixOrthographicLH((float)screenWidth, (float)screenHeight, screenNear, screenDepth);

            CameraClass* m_Camera->SetPosition()

            ModelClass* m_Model->Initialize()

                ModelClass::InitializeBuffers(device);

                    vertices = new VertexType[m_vertexCount];
                    indices = new unsigned long[m_indexCount];
                    D3D11_BUFFER_DESC vertexBufferDesc, indexBufferDesc;
                    ID3D11Device* device->CreateBuffer(&vertexBufferDesc, &vertexData, &m_vertexBuffer);
                    ID3D11Device* device->CreateBuffer(&indexBufferDesc, &indexData, &m_indexBuffer);

                ModelClass::LoadTexture(device, deviceContext, textureFilename);

                    TextureClass* m_Texture->Initialize(device, deviceContext, filename);
                    ID3D11Device* device->CreateTexture2D(&textureDesc, NULL, &m_texture);  // Create the empty texture.
                    ID3D11DeviceContext* deviceContext->UpdateSubresource(m_texture, 0, NULL, m_targaData, rowPitch, 0);  // Copy the targa image data into the texture.
                    ID3D11Device* device->CreateShaderResourceView(m_texture, &srvDesc, &m_textureView);  // Create the shader resource view for the texture.
                    ID3D11DeviceContext* deviceContext->GenerateMips(m_textureView);  // Generate mipmaps for this texture.

            TextureShaderClass* m_TextureShader->Initialize()

                TextureShaderClass::InitializeShader(device, hwnd, L"../source/textureVS.hlsl", L"../source/texturePS.hlsl");

                    D3DCompileFromFile(vsFilename, NULL, NULL, "TextureVertexShader", "vs_5_0", D3D10_SHADER_ENABLE_STRICTNESS, 0, &vertexShaderBuffer, &errorMessage);
                    D3DCompileFromFile(psFilename, NULL, NULL, "TexturePixelShader", "ps_5_0", D3D10_SHADER_ENABLE_STRICTNESS, 0, &pixelShaderBuffer, &errorMessage);
                    ID3D11Device* device->CreateVertexShader(vertexShaderBuffer->GetBufferPointer(), vertexShaderBuffer->GetBufferSize(), NULL, &m_vertexShader);
                    ID3D11Device* device->CreatePixelShader(pixelShaderBuffer->GetBufferPointer(), pixelShaderBuffer->GetBufferSize(), NULL, &m_pixelShader);

                    // Create the vertex input layout description.
                    // This setup needs to match the VertexType stucture in the ModelClass and in the shader.
                    D3D11_INPUT_ELEMENT_DESC polygonLayout[2];  // SemanticName, Format, AlignedByteOffset...
                    ID3D11Device* device->CreateInputLayout(polygonLayout, numElements, vertexShaderBuffer->GetBufferPointer(), vertexShaderBuffer->GetBufferSize(), &m_layout);  // // Create the vertex input layout.


                    // Setup the description of the dynamic matrix constant buffer that is in the vertex shader.
                    D3D11_BUFFER_DESC matrixBufferDesc;  // Usage, ByteWidth, BindFlags, CPUAccessFlags...
                    D3D11Device* device->CreateBuffer(&matrixBufferDesc, NULL, &m_matrixBuffer);  // Create the constant buffer pointer so we can access the vertex shader constant buffer from within this class.

                    // Create a texture sampler state description.
                    D3D11_SAMPLER_DESC samplerDesc;
                    D3D11Device* device->CreateSamplerState(&samplerDesc, &m_sampleState);  // Create the texture sampler state.

    SystemClass* System->Run()

            SystemClass::Frame();

                if(m_Input->IsKeyDown(VK_ESCAPE))

                GraphicsClass* m_Graphics->Frame();  // Do the frame processing for the graphics object.

                    GraphicsClass::Render()

                        // Clear the buffers to begin the scene.
                        D3DClass* m_Direct3D->BeginScene(0.0f, 0.0f, 0.0f, 1.0f);

                            ID3D11DeviceContext* m_deviceContext->ClearRenderTargetView(m_renderTargetView, color);  // Clear the back buffer.
                            ID3D11DeviceContext* m_deviceContext->ClearDepthStencilView(m_depthStencilView, D3D11_CLEAR_DEPTH, 1.0f, 0);  // Clear the depth buffer.

                        // Generate the view matrix based on the camera's position.
                        CameraClass* m_Camera->Render();

                            // Setup the vector that points upwards.
                            // Load it into a XMVECTOR structure.
                            // Setup the position of the camera in the world.
                            // Load it into a XMVECTOR structure.
                            // Setup where the camera is looking by default.
                            // Load it into a XMVECTOR structure.
                            // Set the yaw (Y axis), pitch (X axis), and roll (Z axis) rotations in radians.
                            // Create the rotation matrix from the yaw, pitch, and roll values.
                            // Transform the lookAt and up vector by the rotation matrix so the view is correctly rotated at the origin.
                            // Translate the rotated camera position to the location of the viewer.
                            // Finally create the view matrix from the three updated vectors.

                        // Get the world, view, and projection matrices from the camera and d3d objects.
                        D3DClass* m_Direct3D->GetWorldMatrix(worldMatrix);
                        CameraClass* m_Camera->GetViewMatrix(viewMatrix);
                        D3DClass* m_Direct3D->GetProjectionMatrix(projectionMatrix);

                        // Put the model vertex and index buffers on the graphics pipeline to prepare them for drawing.
                        ModelClass* m_Model->Render(m_Direct3D->GetDeviceContext());

                            // Put the vertex and index buffers on the graphics pipeline to prepare them for drawing.
                            ModelClass::RenderBuffers(deviceContext);

                                // Set the vertex buffer to active in the input assembler so it can be rendered.
                                ID3D11DeviceContext* deviceContext->IASetVertexBuffers(0, 1, &m_vertexBuffer, &stride, &offset);
                                // Set the index buffer to active in the input assembler so it can be rendered.
                                ID3D11DeviceContext* deviceContext->IASetIndexBuffer(m_indexBuffer, DXGI_FORMAT_R32_UINT, 0);
                                // Set the type of primitive that should be rendered from this vertex buffer, in this case triangles.
                                ID3D11DeviceContext* deviceContext->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLESTRIP);

                        // Render the model using the texture shader.
                        TextureShaderClass* m_TextureShader->Render(m_Direct3D->GetDeviceContext(), m_Model->GetIndexCount(), worldMatrix, viewMatrix, projectionMatrix, m_Model->GetTexture());

                            TextureShaderClass::SetShaderParameters(deviceContext, worldMatrix, viewMatrix, projectionMatrix, texture)

                                // Lock the constant buffer so it can be written to.
                                ID3D11DeviceContext* deviceContext->Map(m_matrixBuffer, 0, D3D11_MAP_WRITE_DISCARD, 0, &mappedResource);
                                // Get a pointer to the data in the constant buffer.
                                dataPtr = (MatrixBufferType*)mappedResource.pData;
                                // Copy the matrices into the constant buffer.
                                // Unlock the constant buffer.
                                ID3D11DeviceContext* deviceContext->Unmap(m_matrixBuffer, 0);
                                // Finanly set the constant buffer in the vertex shader with the updated values.
                                ID3D11DeviceContext* deviceContext->VSSetConstantBuffers(bufferNumber, 1, &m_matrixBuffer);
                                // Set shader texture resource in the pixel shader.
                                ID3D11DeviceContext* deviceContext->PSSetShaderResources(0, 1, &texture);

                            TextureShaderClass::RenderShader(deviceContext, indexCount);

                                // Set the vertex input layout.
                                ID3D11DeviceContext* deviceContext->IASetInputLayout(m_layout);
                                // Set the vertex and pixel shaders that will be used to render this triangle.
                                ID3D11DeviceContext* deviceContext->VSSetShader(m_vertexShader, NULL, 0);
                                ID3D11DeviceContext* deviceContext->PSSetShader(m_pixelShader, NULL, 0);
                                // Set the sampler state in the pixel shader.
                                ID3D11DeviceContext* deviceContext->PSSetSamplers(0, 1, &m_sampleState);
                                // Render the triangle.
                                ID3D11DeviceContext* deviceContext->DrawIndexed(indexCount, 0, 0);

                        // Present the back buffer to the screen since rendering is complete.
                        D3DClass* m_Direct3D->EndScene();
                            if (m_vsync_enabled)    IDXGISwapChain* m_swapChain->Present(1, 0);  // Lock to screen refresh rate.
                            else                    IDXGISwapChain* m_swapChain->Present(0, 0);  // Present as fast as possible.


System->Shutdown()


